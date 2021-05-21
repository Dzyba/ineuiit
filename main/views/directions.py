from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Direction

class DirectionView(View):
    template_name = 'main/edupix/direction.html'

    def get(self, request, *args, **kwargs):
        context = {}
        direction = Direction.objects.get(slug=kwargs['slug'])
        menu = Menu.objects.filter(kind=Menu.Kind.DIRECTION_ITEM).first()
        context['header'] = direction.name
        context['sitename'] = Setting.get('sitename')
        context['breadcrumbs'] = direction.get_breadcrumbs_dict(menu)
        context['menus'] = Menu.get_dict()
        context['direction'] = direction
        context['html'] = direction.html
        return render(request, self.template_name, context)