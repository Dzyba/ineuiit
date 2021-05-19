from django.contrib import admin
from main.models import Cathedra


@admin.register(Cathedra)
class CathedraAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('name', 'slug', 'icon', 'image')
    list_display_links = ['name']


