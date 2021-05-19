from django.contrib import admin
from main.models import Staff


class StaffInline(admin.TabularInline):
    model = Staff
    extra = 1
    fields = ['name', 'cathedra', 'position', 'slug', 'category', 'image']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('name', 'cathedra', 'position', 'slug', 'category', 'image')
    list_display_links = ['name']