from django.contrib import admin
from main.models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('name', 'cathedra', 'position', 'category', 'image')
    list_display_links = ['name']