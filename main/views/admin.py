from django.views.generic import View
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.http import HttpResponseRedirect
from main.models import Menu
from django.contrib import messages
from django.urls import reverse
from main.forms import AdminPushForm
from webpush import send_group_notification


class AdminPushView(View):
    template_name = 'admin/push.html'

    def _get_context(self, request, *args, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        context = self._get_context(request, *args, **kwargs)

        ref = request.META.get('HTTP_REFERER', '')
        context['form'] = AdminPushForm(initial={'path': ref})

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'apply' in request.POST:
            push_form = AdminPushForm(request.POST)
            if push_form.is_valid():
                header = push_form.cleaned_data['header']
                text = push_form.cleaned_data['text']

                payload = {
                    'head': header,
                    'body': text,
                    'icon': static('main/img/logo-square.png'),
                    'url': reverse('main:schedules')
                }
                send_group_notification(group_name='all', payload=payload, ttl=1000)

                messages.add_message(request, messages.INFO, 'Уведомление отправлено', extra_tags='', fail_silently=False)
                return HttpResponseRedirect(reverse('admin:main_schedulegroup_changelist'))

        push_form = AdminPushForm(initial={'path': request.get_full_path()})
        return render(request, 'admin/push.html', context={'form': push_form})


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

