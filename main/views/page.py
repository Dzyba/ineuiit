from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Page

class PageView(View):
    template_name = 'main/edupix/page.html'

    def get(self, request, *srgs, **kwargs):
        context = {}

        # print('====>', self.kwargs['slug'])

        page = Page.objects.get(slug=kwargs['slug'])
        context['header'] = page.name
        context['sitename'] = Setting.get('sitename')
        context['menus'] = Menu.get_dict()
        context['page'] = page
        return render(request, self.template_name, context)