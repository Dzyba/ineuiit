from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Cathedra, InnerLink, Staff

class CathedraView(View):
    template_name = 'main/edupix/cathedra.html'

    def get(self, request, *args, **kwargs):
        context = {}
        cathedra = Cathedra.objects.get(slug=kwargs['slug'])
        staff = Staff.objects.filter(cathedra=cathedra)
        context['header'] = cathedra.name
        context['sitename'] = Setting.get('sitename')
        context['menus'] = Menu.get_dict()
        context['cathedra'] = cathedra
        context['inner_links'] = InnerLink.objects.filter(menu__parent__kind=Menu.Kind.CATHEDRA_ITEM)
        return render(request, self.template_name, context)