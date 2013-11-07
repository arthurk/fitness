from django.contrib import admin

from exercise.models import Exercise, Log, Set

class SetInline(admin.TabularInline):
    model = Set
    extra = 1

class LogAdmin(admin.ModelAdmin):
    inlines = (SetInline,)
    list_display = ('day', 'desc',)
    
admin.site.register(Exercise)
admin.site.register(Log, LogAdmin)
