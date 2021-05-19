from django.contrib import admin
from main.models import Page


class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    fields = ['name', 'slug', 'menu', 'html']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    ordering = ['menu__parent', 'menu__name', 'name']
    list_display = ('name', 'menu', 'slug')
    list_display_links = ['name']
