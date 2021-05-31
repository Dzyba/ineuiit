from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Cathedra, InnerLink, Staff
from .index import css_theme


class CathedraView(View):
    template_name = 'main/edupix/cathedra.html'

    def get(self, request, *args, **kwargs):
        context = {}

        cathedra = Cathedra.objects.get(slug=kwargs['slug'])
        staff = Staff.objects.filter(cathedra=cathedra)
        menu = Menu.objects.filter(kind=Menu.Kind.CATHEDRA_ITEM).first()

        context['header'] = cathedra.name
        context['sitename'] = Setting.get('sitename')
        context['theme'] = css_theme(request)
        context['breadcrumbs'] = menu.get_breadcrumbs_dict()
        context['menus'] = Menu.get_dict()
        context['cathedra'] = cathedra
        context['staff'] = staff
        context['inner_links'] = InnerLink.objects.filter(menu__parent__kind=Menu.Kind.CATHEDRA_ITEM)

        return render(request, self.template_name, context)