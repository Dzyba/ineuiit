from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, News

class NewsView(View):
    template_name = 'main/edupix/news.html'

    def get(self, request, *args, **kwargs):
        context = {}
        menu = Menu.objects.filter(kind=Menu.Kind.NEWS_LIST).first()
        page = kwargs['page'] if 'page' in kwargs else 1
        on_page = Setting.get('on_page')
        context['header'] = 'Новости'
        context['sitename'] = Setting.get('sitename')
        context['breadcrumbs'] = menu.get_breadcrumbs_dict()
        context['menus'] = Menu.get_dict()
        context['news'] = News.objects.filter().order_by('-datetime')[(page-1)*on_page:page*on_page]

        news_count = News.objects.all().count()
        pages_count = news_count // on_page + 1

        context['pager'] = {
            'prev': (page-1) if page!=1 else None,
            'next':(page+1) if page!=pages_count else None,
            'page': page,
            'pages': list(range(1, pages_count+1))
        }
        print(context['pager'])

        return render(request, self.template_name, context)

class NewsItemView(View):
    template_name = 'main/edupix/new.html'

    def get(self, request, *args, **kwargs):
        context = {}
        news_item = News.objects.get(slug=kwargs['slug'])
        menu = Menu.objects.filter(kind=Menu.Kind.NEWS_ITEM).first()
        context['header'] = news_item.name
        context['sitename'] = Setting.get('sitename')
        context['breadcrumbs'] = menu.get_breadcrumbs_dict()
        context['menus'] = Menu.get_dict()
        context['news_item'] = news_item
        return render(request, self.template_name, context)