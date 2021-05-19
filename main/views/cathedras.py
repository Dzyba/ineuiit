from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Cathedra, InnerLink

class CathedrasView(View):
    template_name = 'main/edupix/cathedras.html'

    def get(self, request):
        context = {}
        menu = Menu.objects.filter(kind=Menu.Kind.CATHEDRA_LIST).first()
        context['header'] = 'Кафедры'
        context['sitename'] = Setting.get('sitename')
        context['breadcrumbs'] = menu.get_breadcrumbs_dict()
        context['menus'] = Menu.get_dict()
        context['cathedras'] = Cathedra.objects.all()
        return render(request, self.template_name, context)