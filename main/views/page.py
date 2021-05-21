from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Page
from .blocks import Blocks

class PageView(View):
    template_name = 'main/edupix/page.html'

    def get(self, request, *srgs, **kwargs):
        page = Page.objects.get(slug=kwargs['slug'])

        context = {}
        context['header'] = page.name
        context['breadcrumbs'] = page.menu.get_breadcrumbs_dict()
        context['sitename'] = Setting.get('sitename')
        context['menus'] = Menu.get_dict()
        context['page'] = page
        context['html'] = page.html.format(
            block_directions_p=Blocks.block_directions_p(),
            block_directions_table=Blocks.block_directions_table(),
        )

        if page.is_sidebar:
            context['sidebar'] = {
                'header': page.sidebar_name if page.sidebar_name else None,
                'objects': page.menu.childs
            }
        return render(request, self.template_name, context)