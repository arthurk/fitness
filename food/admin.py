from django.contrib import admin
from django import forms
from django.forms import ModelForm

from food.models import Food, Recipe, Ingredient, Log, FoodLog, Serving, \
    Goal, UNIT_CHOICES


class ServingInline(admin.TabularInline):
    model = Serving
    extra = 0


class FoodAdmin(admin.ModelAdmin):
    inlines = (ServingInline,)
    view_on_site = False


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('name', 'kcal', 'protein', 'carbs', 'fat')
    view_on_site = False

    def kcal(self, obj):
        return int(round(obj.totals()['kcal']))

    def protein(self, obj):
        return int(round(obj.totals()['protein']))

    def carbs(self, obj):
        return int(round(obj.totals()['carbs']))

    def fat(self, obj):
        return int(round(obj.totals()['fat']))


class FoodLogInlineForm(ModelForm):
    unit = forms.ChoiceField(label='Unit', choices=UNIT_CHOICES)

    def __init__(self, *args, **kwargs):
        super(FoodLogInlineForm, self).__init__(*args, **kwargs)
        food = kwargs.get('instance')

        # existing entry
        if food:
            custom_servings = food.food.serving_set.all()

            # add custom servings to unit choices
            self.fields['unit'].choices += [
                (s.id, '%s (%s %s)' % (s.name, s.amount, s.food.unit))
                for s in custom_servings]

            # try to guess if the user logged a custom serving
            # (the data in the db is saved as mg/g/ml or l)
            if custom_servings:
                for serving in custom_servings:
                    p = float(self.initial['amount']) / float(serving.amount)
                    if p.is_integer():
                        self.initial['amount'] = int(p)
                        self.initial['unit'] = serving.id
                        break
        # saving new entry
        else:
            # add servings to choices (for validation)
            data = kwargs.get('data')
            if data:
                food_id = data[kwargs.get('prefix') + '-food']
                food = Food.objects.select_related('serving').get(id=food_id)
                choices = food.serving_set.values_list('id', 'name')
                self.fields['unit'].choices += choices

    def clean(self):
        cleaned_data = self.cleaned_data
        # convert serving to a real unit (e.g. mg/g/ml/L)
        try:
            # if the unit is an integer, it is a Serving id
            serving_id = int(cleaned_data['unit'])
            serving = Serving.objects.get(id=serving_id)
            cleaned_data['amount'] = serving.amount * cleaned_data['amount']
            cleaned_data['unit'] = serving.unit
        except:
            pass
        return cleaned_data

    class Meta:
        model = FoodLog


class FoodLogInline(admin.TabularInline):
    model = FoodLog
    form = FoodLogInlineForm
    extra = 0
    readonly_fields = ('kcal', 'protein', 'carbs', 'fat')
    template = 'tabular.html'

    def kcal(self, obj):
        return int(round(obj.totals()['kcal']))

    def protein(self, obj):
        return int(round(obj.totals()['protein']))

    def carbs(self, obj):
        return int(round(obj.totals()['carbs']))

    def fat(self, obj):
        return int(round(obj.totals()['fat']))


class LogAdmin(admin.ModelAdmin):
    save_as = True
    inlines = (FoodLogInline,)
    list_display = ('day', 'kcal', 'protein', 'carbs', 'fat')
    view_on_site = False

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['recipes'] = Recipe.objects.all()
        return super(LogAdmin, self).add_view(
            request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['recipes'] = Recipe.objects.all()
        extra_context['log'] = Log.objects.get(pk=object_id)
        return super(LogAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context)

    def kcal(self, obj):
        return int(round(obj.totals()['kcal']))

    def protein(self, obj):
        return int(round(obj.totals()['protein']))

    def carbs(self, obj):
        return int(round(obj.totals()['carbs']))

    def fat(self, obj):
        return int(round(obj.totals()['fat']))


class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'goal', 'value',
                    'value2')

admin.site.register(Food, FoodAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Goal, GoalAdmin)
