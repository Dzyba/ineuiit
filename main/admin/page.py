from django.contrib import admin
from main.models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    ordering = ['menu__parent', 'menu__name', 'name']
    list_display = ('name', 'menu', 'slug')
    list_display_links = ['name']
    readonly_fields = ['slug']

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False

