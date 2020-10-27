from django.contrib import admin
from .models import Test


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'interval', 'coverage',)
    list_display_links = ('id', 'interval', 'coverage',)
    ordering = ('id',)
    list_per_page = 25


admin.site.register(Test, TestAdmin)
