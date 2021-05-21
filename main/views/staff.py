from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Staff

class StaffView(View):
    template_name = 'main/edupix/staff.html'

    def get(self, request, *args, **kwargs):
        context = {}
        staff = Staff.objects.get(slug=kwargs['slug'])
        menu = Menu.objects.filter(kind=Menu.Kind.CATHEDRA_ITEM).first()
        context['header'] = staff.name
        context['sitename'] = Setting.get('sitename')
        context['breadcrumbs'] = staff.get_breadcrumbs_dict(menu)
        context['menus'] = Menu.get_dict()
        context['staff'] = staff
        context['html'] = staff.html
        return render(request, self.template_name, context)