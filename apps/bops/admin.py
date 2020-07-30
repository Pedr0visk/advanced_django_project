from django.contrib import admin
from .models import Bop

class BopAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'code', 'created_at', 'updated_at')
  list_display_links = ('id', 'name', 'code')
  search_fields = ('name', 'code',)
  list_per_page = 25
  

admin.site.register(Bop, BopAdmin)