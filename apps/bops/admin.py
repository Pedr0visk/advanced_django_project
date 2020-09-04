from django.contrib import admin
from .models import Bop, Rig, SafetyFunction, Test, TestGroup


class BopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('id', 'name',)
    list_per_page = 25


admin.site.register(Bop, BopAdmin)


class RigAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    list_per_page = 25


admin.site.register(Rig, RigAdmin)


class SafetyFunctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    list_per_page = 25


admin.site.register(SafetyFunction, SafetyFunctionAdmin)


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'interval', 'coverage',)
    list_display_links = ('id', 'interval', 'coverage',)
    search_fields = ('interval', 'coverage',)
    ordering = ('id', 'interval',)
    list_per_page = 25


admin.site.register(Test, TestAdmin)


class TestGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'code',)
    list_display_links = ('id', 'code',)
    list_per_page = 25


admin.site.register(TestGroup, TestGroupAdmin)
