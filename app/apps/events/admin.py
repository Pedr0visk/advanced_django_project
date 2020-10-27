from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description', 'type')
  list_display_links = ('id', 'name')
  search_fields = ('name', 'description', )
  list_per_page = 25

admin.site.register(Event, EventAdmin)