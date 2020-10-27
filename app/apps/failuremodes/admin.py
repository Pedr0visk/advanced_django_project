from django.contrib import admin

from .models import FailureMode


class FailureModeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    list_display_links = ('id', 'code',)
    list_per_page = 25


admin.site.register(FailureMode, FailureModeAdmin)
