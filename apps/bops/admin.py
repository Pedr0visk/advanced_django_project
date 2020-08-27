from django.contrib import admin
from .models import Bop, FailureMode


class BopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    list_per_page = 25


admin.site.register(Bop, BopAdmin)


class FailureModeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'distribution',)
    list_display_links = ('id', 'name', 'code',)
    list_per_page = 25


admin.site.register(FailureMode, FailureModeAdmin)
