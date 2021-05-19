from django.contrib import admin
from main.models import Menu, Page, FileObject, InnerLink, Cathedra, Staff
from django.contrib.admin.views.decorators import staff_member_required
from main.views import AdminMenuOrderUpView, AdminMenuOrderDownView
from django.urls import reverse, path
from django.utils.html import escape, mark_safe, format_html
from .page import PageInline

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    ordering = ['order']

    list_display = ('admin_str', 'parent', 'order_actions', 'kind', 'kind_obj') # order
    list_display_links = ['admin_str']
    # readonly_fields = ['order']

    # inlines = [PageInline, FileObjectInline, InnerLinkInline]

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

    def kind_obj(self, obj):
        error_tag = '<span style="color:red;">%s</span>'
        warning_tag = '<span style="color:yellow;">%s</span>'
        if obj.kind == Menu.Kind.DEFAULT:
            return '-'
        elif obj.kind == Menu.Kind.INDEX:
            try:
                page = Page.objects.get(slug='index', menu=obj)
                link = reverse('admin:main_page_change', args=[page.id])
                return mark_safe('<a href="%s">%s</a>' % (link, 'страница'))
            except Page.DoesNotExist:
                return mark_safe(error_tag % ('нет страницы'))
            except Page.MultipleObjectsReturned:
                return mark_safe(error_tag % ('дублирование страниц'))

        elif obj.kind == Menu.Kind.PAGE or obj.kind == Menu.Kind.GROUP_PAGE:
            try:
                page = Page.objects.get(menu=obj)
                link = reverse('admin:main_page_change', args=[page.id])
                return mark_safe('<a href="%s">%s</a>' % (link, 'страница'))
            except Page.DoesNotExist:
                return mark_safe(error_tag % ('нет страницы'))
            except Page.MultipleObjectsReturned:
                return mark_safe(error_tag % ('дублирование страниц'))

        elif obj.kind == Menu.Kind.GROUP:
            return '-'

        elif obj.kind == Menu.Kind.FILEOBJECT:
            try:
                file_object = FileObject.objects.get(menu=obj)
                link = reverse('admin:main_fileobject_change', args=[file_object.id])
                return mark_safe('<a href="%s">%s</a>' % (link, 'файл'))
            except FileObject.DoesNotExist:
                return mark_safe(error_tag % ('нет файла'))
            except FileObject.MultipleObjectsReturned:
                return mark_safe(error_tag % ('дублирование файлов'))

        elif obj.kind == Menu.Kind.INNER_LINK:
            try:
                inner_link = InnerLink.objects.get(menu=obj)
                link = reverse('admin:main_innerlink_change', args=[inner_link.id])
                return mark_safe('<a href="%s">%s</a>' % (link, 'внутренняя ссылка'))
            except InnerLink.DoesNotExist:
                return mark_safe(error_tag % ('нет внутренней ссылки'))
            except InnerLink.MultipleObjectsReturned:
                return mark_safe(error_tag % ('дублирование внутренних ссылок'))

        elif obj.kind == Menu.Kind.CATHEDRA_LIST or obj.kind == Menu.Kind.CATHEDRA_ITEM:
            cathedras_count = Cathedra.objects.all().count()
            if cathedras_count:
                link = reverse('admin:main_cathedra_changelist')
                return mark_safe('<a href="%s">кафедры <b>%s</b> шт.</a>' % (link, cathedras_count))
            else:
                return mark_safe(error_tag % ('нет кафедр'))

        elif obj.kind == Menu.Kind.STAFF_ITEM:
            staff_count = Staff.objects.all().count()
            if staff_count:
                link = reverse('admin:main_staff_changelist')
                return mark_safe('<a href="%s">сотрудники <b>%s</b> шт.</a>' % (link, staff_count))
            else:
                return mark_safe(error_tag % ('нет сотрудников'))

        return '-'

    # SCHEDULE = 'schedule', 'Расписание'
    # DIRECTION_ITEM = 'direction', 'Направление'

    kind_obj.short_description = 'Объект'