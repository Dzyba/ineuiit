from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu, Page, News, Announcement

def css_theme(request):
    try:
        theme = request.session['theme']
    except:
        return 'common'
    return 'contrast' if theme == 'contrast' else 'common'

class IndexView(View):
    template_name = 'main/edupix/index.html'

    def get(self, request):
        context = {}
        # page = Page.objects.get(slug='index')
        # context['header'] = page.name
        # context['breadcrumbs'] = page.menu.get_breadcrumbs_dict()
        # context['page'] = page

        context['sitename'] = Setting.get('sitename')
        context['theme'] = css_theme(request)
        context['menus'] = Menu.get_dict()
        context['slider'] = News.objects.filter(is_slider=True).order_by('-datetime')[:3]
        context['news'] = News.objects.filter().order_by('-datetime')[:3]
        announcements = Announcement.objects.all().order_by('-datetime')[:4]
        context['announcement'] = announcements[0]
        context['announcements'] = announcements[1:4]
        return render(request, self.template_name, context)