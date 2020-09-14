from django.contrib import admin
from .models import TestGroup


class TestGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date')
    list_display_links = ('id', 'start_date',)
    list_per_page = 25


admin.site.register(TestGroup, TestGroupAdmin)
