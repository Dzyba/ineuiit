from django.contrib import admin
from main.models import FileObject


@admin.register(FileObject)
class FileObjectAdmin(admin.ModelAdmin):
    ordering = ['menu__parent', 'menu__name', 'name']
    list_display = ('name', 'menu', 'slug', 'object')
    list_display_links = ['name']

