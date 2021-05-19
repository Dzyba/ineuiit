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

class CathedraView(View):
    template_name = 'main/edupix/cathedra.html'

    def get(self, request, *srgs, **kwargs):
        context = {}
        cathedra = Cathedra.objects.get(slug=kwargs['slug'])
        context['header'] = cathedra.name
        context['sitename'] = Setting.get('sitename')
        context['menus'] = Menu.get_dict()
        context['cathedra'] = cathedra
        context['inner_links'] = InnerLink.objects.filter(menu__parent__kind=Menu.Kind.CATHEDRA_ITEM)
        return render(request, self.template_name, context)