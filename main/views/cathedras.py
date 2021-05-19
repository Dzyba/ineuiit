from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Cathedra, InnerLink

class CathedrasView(View):
    template_name = 'main/edupix/cathedras.html'

    def get(self, request):
        context = {}
        context['header'] = 'Кафедры'
        context['sitename'] = Setting.get('sitename')
        context['menus'] = Menu.get_dict()
        context['cathedras'] = Cathedra.objects.all()
        return render(request, self.template_name, context)