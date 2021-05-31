from django.shortcuts import redirect
from django.views import View


class ThemeView(View):
    def get(self, request, *args, **kwargs):
        if 'slug' in kwargs:
            request.session['theme'] = kwargs['slug']
        return redirect('main:index')