from django.contrib import admin
from .models import Campaign, Phase, Schema


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'active')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Phase)
admin.site.register(Schema)

