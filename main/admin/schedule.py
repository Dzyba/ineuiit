from django.contrib import admin
from main.models import ScheduleGroup, ScheduleDay, ScheduleTimeSlot
from django.urls import reverse
from django.utils.html import escape, mark_safe

class ScheduleDayInline(admin.TabularInline):
    model = ScheduleDay
    extra = 0
    fields = ['number', 'name', 'group']

class ScheduleTimeSlotInline(admin.TabularInline):
    model = ScheduleTimeSlot
    extra = 0
    fields = ['number', 'time', 'day', 'pair', 'appearance']

@admin.register(ScheduleGroup)
class ScheduleGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'message')
    list_display_links = ['name', 'slug']

    inlines = [ScheduleDayInline]

@admin.register(ScheduleDay)
class ScheduleDayAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'group_link')
    list_display_links = ['number', 'name']

    inlines = [ScheduleTimeSlotInline]

    def group_link(self, obj):
        if not obj.group_id:
            return '-'
        link = reverse('admin:main_schedulegroup_change', args=[obj.group_id])
        return mark_safe(f'<a href="{link}">{escape(obj.group.__str__())}</a>')
    group_link.short_description = 'Группа'
    group_link.admin_order_field = 'group'

@admin.register(ScheduleTimeSlot)
class ScheduleTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('number', 'time', 'day_link', 'group_link', 'pair', 'appearance')
    list_display_links = ['number', 'time']

    def day_link(self, obj):
        if not obj.day_id:
            return '-'
        link = reverse('admin:main_scheduleday_change', args=[obj.day_id])
        return mark_safe(f'<a href="{link}">{escape(obj.day.name)}</a>')
    day_link.short_description = 'Учебный день'
    day_link.admin_order_field = 'day'

    def group_link(self, obj):
        if not obj.day_id:
            return '-'
        if not obj.day.group_id:
            return '-'
        link = reverse('admin:main_schedulegroup_change', args=[obj.day.group_id])
        return mark_safe(f'<a href="{link}">{escape(obj.day.group.__str__())}</a>')
    group_link.short_description = 'Группа'
    group_link.admin_order_field = 'group'