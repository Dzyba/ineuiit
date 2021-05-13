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
        context['menu'] = Menu.objects.all().order_by('order')
        context['page'] = page
        return render(request, self.template_name, context)