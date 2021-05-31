from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Announcement
from .index import css_theme


class AnnouncementsView(View):
    template_name = 'main/edupix/announcements.html'

    def get(self, request, *args, **kwargs):
        context = {}
        menu = Menu.objects.filter(kind=Menu.Kind.ANNOUNCEMENT_LIST).first()
        page = kwargs['page'] if 'page' in kwargs else 1
        on_page = Setting.get('on_page')
        context['header'] = 'Анонсы'
        context['sitename'] = Setting.get('sitename')
        context['theme'] = css_theme(request)
        context['breadcrumbs'] = menu.get_breadcrumbs_dict()
        context['menus'] = Menu.get_dict()
        context['announcements'] = Announcement.objects.filter().order_by('-datetime')[(page-1)*on_page:page*on_page]

        announcements_count = Announcement.objects.all().count()
        pages_count = announcements_count // on_page + 1

        context['pager'] = {
            'prev': (page-1) if page!=1 else None,
            'next':(page+1) if page!=pages_count else None,
            'page': page,
            'pages': list(range(1, pages_count+1))
        }
        print(context['pager'])

        return render(request, self.template_name, context)

class AnnouncementsItemView(View):
    template_name = 'main/edupix/announcement.html'

    def get(self, request, *args, **kwargs):
        context = {}
        announcement = Announcement.objects.get(slug=kwargs['slug'])
        menu = Menu.objects.filter(kind=Menu.Kind.ANNOUNCEMENT_ITEM).first()
        context['header'] = announcement.name
        context['sitename'] = Setting.get('sitename')
        context['theme'] = css_theme(request)
        context['breadcrumbs'] = menu.get_breadcrumbs_dict()
        context['menus'] = Menu.get_dict()
        context['announcement'] = announcement
        return render(request, self.template_name, context)