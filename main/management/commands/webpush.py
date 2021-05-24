from django.core.management.base import BaseCommand
from webpush import send_group_notification

class Command(BaseCommand):
    help = 'Send web push notification'

    def handle(self, *args, **options):
        payload = {
            'head': 'Тест сообщения',
            'body': 'Тест сообщения, текст',
            # 'icon': 'https://i.imgur.com/dRDxiCQ.png',
            # 'url': 'https://www.example.com'
        }
        send_group_notification(group_name='grp001', payload=payload, ttl=1000)
