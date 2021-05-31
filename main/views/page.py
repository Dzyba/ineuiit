from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Page, PageImage
from .blocks import Blocks
from .staff import Staff
from .index import css_theme


class PageView(View):
    template_name = 'main/edupix/page.html'

    def get(self, request, *args, **kwargs):
        page = Page.objects.get(slug=kwargs['slug'])
        page_images = PageImage.objects.filter(page=page)
        html = page.html.format(
            block_directions_p=Blocks.block_directions_p(),
            block_directions_table=Blocks.block_directions_table(),
            block_staff_table_deanery=Blocks.block_staff_table([Staff.Category.DEANERY]),
            block_staff_table_council=Blocks.block_staff_table([Staff.Category.COUNCIL]),
            **{'image_url_%s' % (page_image.slug):page_image.image.url for page_image in page_images }
        )

        context = {}
        context['header'] = page.name
        context['breadcrumbs'] = page.menu.get_breadcrumbs_dict()
        context['sitename'] = Setting.get('sitename')
        context['theme'] = css_theme(request)
        context['menus'] = Menu.get_dict()
        context['page'] = page
        context['html'] = html

        if page.is_sidebar:
            context['sidebar'] = {
                'header': page.sidebar_name if page.sidebar_name else None,
                'objects': page.menu.childs
            }
        return render(request, self.template_name, context)