from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Staff

class StaffView(View):
    template_name = 'main/edupix/staff.html'

    def get(self, request, *args, **kwargs):
        context = {}
        staff = Staff.objects.get(slug=kwargs['slug'])
        context['header'] = staff.name
        context['sitename'] = Setting.get('sitename')
        context['menus'] = Menu.get_dict()
        context['staff'] = staff
        return render(request, self.template_name, context)