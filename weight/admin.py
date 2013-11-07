from django.contrib import admin

from weight.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('day', 'bodyweight',)
    change_list_template = 'change_list.html'

admin.site.register(Log, LogAdmin)
