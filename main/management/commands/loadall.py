from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
import os, shutil

class Command(BaseCommand):
    help = 'Load all fixtures'

    def handle(self, *args, **options):
        # Загрузка данных
        fixtures = sorted(os.listdir('main/fixtures'))
        excludes = ['01_menus_test.json']
        for fixture in fixtures:
            if fixture not in excludes:
                execute_from_command_line(['manage.py', 'loaddata', fixture])

        # Копирование _media
        shutil.copytree('_media', 'media', dirs_exist_ok=True)
