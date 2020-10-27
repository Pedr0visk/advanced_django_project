from django.contrib import admin
from .models import Cut


class CutAdmin(admin.ModelAdmin):
    list_display = ('id', 'index', 'order',)
    list_display_links = ('id', 'index',)
    ordering = ('id', 'index',)
    list_per_page = 25


admin.site.register(Cut, CutAdmin)
