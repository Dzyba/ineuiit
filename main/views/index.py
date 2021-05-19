from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Page

class IndexView(View):
    template_name = 'main/edupix/index.html'

    def get(self, request):
        context = {}
        page = Page.objects.get(slug='index')
        context['header'] = page.name
        context['sitename'] = Setting.get('sitename')
        context['breadcrumbs'] = page.menu.get_breadcrumbs_dict()
        context['menus'] = Menu.get_dict()
        context['page'] = page
        return render(request, self.template_name, context)