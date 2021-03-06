from django.contrib import admin
from django.shortcuts import render
from main.models import ScheduleGroup, ScheduleDay, ScheduleTimeSlot
from django.urls import path, reverse
from django.utils.html import escape, mark_safe
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from main.views import AdminPushView
from main.forms import AdminPushForm
from webpush import send_group_notification
from django.templatetags.static import static


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
    fields = ['number', 'time', 'day', 'pair_numerator', 'pair_denominator', 'is_whole']

@admin.register(ScheduleGroup)
class ScheduleGroupAdmin(admin.ModelAdmin):
    change_list_template = 'admin/schedulegroup_change_list.html'

    list_display = ('name', 'slug', 'message', 'export')
    list_display_links = ['name', 'slug']

    inlines = [ScheduleDayInline]

    # actions=['push']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('push', staff_member_required(AdminPushView.as_view()), name='push'),
        ]
        return custom_urls + urls

    def push(self, request, queryset):
        if 'apply' in request.POST:
            push_form = AdminPushForm(request.POST)
            if push_form.is_valid():
                header = push_form.cleaned_data['header']
                text = push_form.cleaned_data['text']

                payload = {
                    'head': header,
                    'body': text,
                    'icon': static('main/img/logo-square.png'),
                    'url': reverse('main:schedules')
                }
                send_group_notification(group_name='all', payload=payload, ttl=1000)

                self.message_user(request, 'Уведомление отправлено')
                return HttpResponseRedirect(reverse('admin:main_schedulegroup_changelist'))

        push_form = AdminPushForm(initial={'path':request.get_full_path()})
        return render(request, 'admin/push.html', context={'form':push_form, 'groups': queryset})
    push.short_description = 'Послать уведомление'

    def export(self, obj):
        link = reverse('main:schedule-export', args=[obj.slug])
        return mark_safe(f'<a class="button" href="{link}">Расписание .xlsx</a>')
    export.short_description = 'Экспорт XLSX'

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
    list_display = ('number', 'time', 'day_link', 'group_link', 'pair_numerator', 'pair_denominator', 'is_whole')
    list_display_links = ['number', 'time']

    def day_link(self, obj):
        if not obj.day_id:
            return '-'
        link = reverse('admin:main_scheduleday_change', args=[obj.day_id])
        return mark_safe(f'<a href="{link}">{escape(obj.day.get_day_display())}</a>')
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