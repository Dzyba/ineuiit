from django.contrib import admin
from main.models import Menu
from django.contrib.admin.views.decorators import staff_member_required
from main.views import AdminMenuOrderUpView, AdminMenuOrderDownView
from django.urls import reverse, path
from django.utils.html import escape, mark_safe, format_html

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    ordering = ['order']

    list_display = ('name', 'admin_str', 'parent', 'order_actions')
    list_display_links = ['name']
    readonly_fields = ['order']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin/menu/order/up/<int:id>', staff_member_required(AdminMenuOrderUpView.as_view()), name='menu-order-up'),
            path('admin/menu/order/down/<int:id>', staff_member_required(AdminMenuOrderDownView.as_view()), name='menu-order-down')
        ]
        return custom_urls + urls

    def order_actions(self, obj):
        if obj.level:
            if obj.order_in_parent_is_first:
                button_up = '<a class="button" href="{}" style="background: #bbb;">▲</a>'
                link_up = 'javascript:void(0);'
            else:
                button_up = '<a class="button" href="{}">▲</a>'
                link_up = reverse('admin:menu-order-up', args=[obj.pk])
            if obj.order_in_parent_is_last:
                button_down = '<a class="button disabled" href="{}" style="background: #bbb;">▼</a>'
                link_down = 'javascript:void(0);'
            else:
                button_down = '<a class="button" href="{}">▼</a>'
                link_down = reverse('admin:menu-order-down', args=[obj.pk])
            return format_html('%s %s' % (button_up, button_down), link_up, link_down)
        else:
            return '-'
    order_actions.short_description = 'Порядок'

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False