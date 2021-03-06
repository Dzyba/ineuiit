from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, ScheduleGroup, ScheduleDay, ScheduleTimeSlot
from django.utils import translation
from .index import css_theme


class ScheduleView(View):
    template_name = 'main/edupix/schedule.html'

    def get(self, request, *args, **kwargs):
        translation.activate('ru')

        context = {}
        groups = ScheduleGroup.objects.all()
        context['groups'] = groups
        menu = Menu.objects.filter(kind=Menu.Kind.SCHEDULE).first()
        if 'slug' not in kwargs:
            context['is_list'] = True
            context['header'] = 'Расписание'
            context['breadcrumbs'] = menu.get_breadcrumbs_dict()
        else:
            context['is_list'] = False
            group = ScheduleGroup.objects.get(slug=kwargs['slug'])

            context['header'] = 'Расписание ' + group.name
            context['breadcrumbs'] = group.get_breadcrumbs_dict(menu)
            context['group'] = group
            context['webpush'] = {'group': 'all'}
            context['schedule'] = group.get_schedule_dict()

        menu = Menu.objects.filter(kind=Menu.Kind.CATHEDRA_ITEM).first()

        context['sitename'] = Setting.get('sitename')
        context['theme'] = css_theme(request)
        context['menus'] = Menu.get_dict()
        return render(request, self.template_name, context)