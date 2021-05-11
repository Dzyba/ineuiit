from django.contrib import admin
from main.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'slug', 'value')
    list_display_links = ['id', 'name']
    readonly_fields = ['name', 'slug']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False