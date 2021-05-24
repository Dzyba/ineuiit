from django.views.generic import View
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from main.models import Menu
from django.contrib import messages
from django.urls import reverse
from main.forms import AdminPushForm
from main.models import ScheduleGroup

class AdminPushView(View):
    template_name = 'admin/add_to_task.html'

    def _get_context(self, request, *args, **kwargs):
        ref = request.META.get('HTTP_REFERER', '')
        context = {
            'form': AdminPushForm(initial={'path':ref}),
            'groups':ScheduleGroup.objects.filter(id=kwargs['id'])
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self._get_context(request, *args, **kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass
        # if 'apply' in request.POST:
        #     task_form = PushForm(request.POST)
        #     if task_form.is_valid():
        #         task = task_form.cleaned_data['task']
        #         if task == None:
        #             task = Task.objects.create()
        #         Placement.objects.filter(id=kwargs['id']).update(task=task)
        #
        #         messages.add_message(
        #             request,
        #             messages.INFO,
        #             'Заявка добавлена в задание',
        #             extra_tags='',
        #             fail_silently=False
        #         )
        #         # return HttpResponseRedirect(task_form.cleaned_data['path'])
        #         return HttpResponseRedirect(reverse('admin:main_task_change', args=[task.id]))


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

