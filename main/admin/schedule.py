from django.contrib import admin
from main.models import ScheduleGroup, ScheduleDay, ScheduleTimeSlot
from django.urls import reverse
from django.utils.html import escape, mark_safe

class ScheduleDayInline(admin.TabularInline):
    model = ScheduleDay
    extra = 0
    fields = ['day', 'schedule', 'day_link', 'group']
    readonly_fields = ['schedule', 'day_link']

    def schedule(self, obj):
        timeslots = ScheduleTimeSlot.objects.filter(day=obj).order_by('number')
        html = ''
        for timeslot in timeslots:
            if timeslot.appearance == ScheduleTimeSlot.Appearance.ALWAYS:
                html += '<tr><td>%s</td><td colspan="2">%s</td></tr>' %(timeslot.time, timeslot.pair)
            elif timeslot.appearance == ScheduleTimeSlot.Appearance.NUMERATOR:
                html += '<tr><td>%s</td><td>%s</td><td></td></tr>' % (timeslot.time, timeslot.pair)
            elif timeslot.appearance == ScheduleTimeSlot.Appearance.DENOMINATOR:
                html += '<tr><td>%s</td><td></td><td>%s</td></tr>' % (timeslot.time, timeslot.pair)
        html = '<table><tbody>%s</tbody></table>' %(html)
        return mark_safe(html)
    schedule.short_description = 'Расписание'

    def day_link(self, obj):
        link = reverse('admin:main_scheduleday_change', args=[obj.id])
        return mark_safe(f'<a href="{link}">редактировать</a>')
    day_link.short_description = 'Действия'

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
    list_display = ('day', 'group_link')
    list_display_links = ['day']

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