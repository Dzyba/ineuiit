from django.views.generic import View
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from main.models import Menu
from django.contrib import messages
from django.urls import reverse


# Вспомогательные функции сообщений и редиректа
def _message(request, message, status=messages.INFO):
    messages.add_message(request, status, message, extra_tags='', fail_silently=False)
    return redirect('admin:main_menu_changelist')

def _error(request, message='Не удалось изменить порядок'):
    return _message(request, message, messages.ERROR)


class AdminMenuOrderUpView(View):
    def get(self, request, *args, **kwargs):
        if not 'id' in kwargs:
            return _error(request)
        try:
            menu = Menu.objects.get(id=kwargs['id'])
        except:
            return _error(request)
        if not menu.parent:
            return _error(request)

        if menu.order_in_parent > 1:
            menu.order_up()
        else:
            return _error(request, 'Порядок уже первый в своём пункте, возможно вам надо изменить родительский пункт')

        return _message(request, 'Порядок изменён вверх')

class AdminMenuOrderDownView(View):
    def get(self, request, *args, **kwargs):
        if not 'id' in kwargs:
            return _error(request)
        try:
            menu = Menu.objects.get(id=kwargs['id'])
        except:
            return _error(request)
        if not menu.parent:
            return _error(request)

        if not menu.order_in_parent_is_last:
            menu.order_down()
        else:
            return _error(request, 'Порядок уже последний в своём пункте, возможно вам надо изменить родительский пункт')

        return _message(request, 'Порядок изменён вниз')

