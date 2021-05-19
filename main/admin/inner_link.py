from django.contrib import admin
from main.models import InnerLink


class InnerLinkInline(admin.TabularInline):
    model = InnerLink
    extra = 0
    fields = ['name', 'slug', 'menu']

@admin.register(InnerLink)
class InnerLinkAdmin(admin.ModelAdmin):
    ordering = ['menu__parent', 'menu__name', 'name']
    list_display = ('name', 'menu', 'slug')
    list_display_links = ['name']
