from django.contrib import admin
from django.shortcuts import render
from main.models import ScheduleGroup, ScheduleDay, ScheduleTimeSlot
from django.urls import path, reverse
from django.utils.html import escape, mark_safe
from django.contrib.admin.views.decorators import staff_member_required
from main.views import AdminPushView
from main.forms import AdminPushForm

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
    list_display = ('name', 'slug', 'message')
    list_display_links = ['name', 'slug']

    inlines = [ScheduleDayInline]

    actions=['push']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin/main/schedulegroup/push/<int:id>', staff_member_required(AdminPushView.as_view()), name='admin-push'),
        ]
        return custom_urls + urls

    def push(self, request, queryset):
        # if 'apply' in request.POST:
        #     task_form = AdminTaskForm(request.POST)
        #     if task_form.is_valid():
        #         task = task_form.cleaned_data['task']
        #         # if task == None:
        #         #     task = Task.objects.create()
        #         queryset.update(task=task)
        #         self.message_user(request, '{} заявок добавлено в задание'.format(queryset.count()))
        #         return HttpResponseRedirect(task_form.cleaned_data['path'])
        #         # return HttpResponseRedirect(reverse('admin:main_task_change', args=[task.id]))

        push_form = AdminPushForm(initial={'path':request.get_full_path()})
        return render(request, 'admin/push.html', context={'form':push_form, 'groups': queryset})
    push.short_description = 'Послать уведомление'

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