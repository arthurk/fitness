from django.contrib import admin

from food.models import Food, Recipe, Ingredient, Log, FoodLog, Serving

class ServingInline(admin.TabularInline):
    model = Serving
    extra = 1

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

class FoodLogInline(admin.TabularInline):
    model = FoodLog
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

admin.site.register(Food, FoodAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Log, LogAdmin)
