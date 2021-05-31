from django.shortcuts import render
from django.views import View
from main.models import Setting, Menu
from main.forms import CertificateOrderForm
from .index import css_theme

import smtplib
from email.mime.text import MIMEText
from email.header import Header

class CertificatesView(View):
    template_name = 'main/edupix/certificates.html'

    def _get_context(self, request, *args, **kwargs):
        context = {}
        context['header'] = 'Заказ справок'
        context['breadcrumbs'] = Menu.objects.filter(kind=Menu.Kind.CERTIFICATES).first().get_breadcrumbs_dict()
        context['sitename'] = Setting.get('sitename')
        context['theme'] = css_theme(request)
        context['menus'] = Menu.get_dict()

        return context

    def get(self, request, *args, **kwargs):
        context = self._get_context(request, *args, **kwargs)
        context['form'] = CertificateOrderForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self._get_context(request, *args, **kwargs)
        context['form'] = CertificateOrderForm(request.POST)
        if context['form'].is_valid():

            # Отправка почты
            to = Setting.get('reciever_email')
            subject = 'Заказ справки от {name} ({group})'.format(
                name=context['form'].cleaned_data['name'],
                group=context['form'].cleaned_data['group']
            )
            body = '<p>Фамилия и имя: {name}</p><p>Email: {email}</p><p>Группа: {group}</p><p>Необходимая справка: {certificate}</p>'.format(
                name=context['form'].cleaned_data['name'],
                email=context['form'].cleaned_data['email'],
                group=context['form'].cleaned_data['group'],
                certificate=context['form'].cleaned_data['certificate'].name
            )
            _mail(to, subject, body)

            context['success'] = True
        return render(request, self.template_name, context)

# Отправка почты -------------------------------------------------------------------------------------------------------
def _mail(to, subject, body):
    # smtp_host = 'smtp.live.com'        # microsoft
    # smtp_host = 'smtp.gmail.com'       # google
    # smtp_host = 'smtp.mail.yahoo.com'  # yahoo
    # smtp_host = 'smtp.yandex.ru'       # yandex
    smtp_host = Setting.get('sender_email_smtp')
    login, password = Setting.get('sender_email'), Setting.get('sender_email_password')
    recipients_emails = [to]

    msg = MIMEText(body, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = login
    msg['To'] = ", ".join(recipients_emails)

    smtp = smtplib.SMTP(smtp_host, 587, timeout=10)
    smtp.set_debuglevel(1)
    try:
        smtp.starttls()
        smtp.login(login, password)
        smtp.sendmail(msg['From'], recipients_emails, msg.as_string())
    finally:
        smtp.quit()