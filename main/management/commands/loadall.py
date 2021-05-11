from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
import os

class Command(BaseCommand):
    help = 'Load all fixtures'

    def handle(self, *args, **options):
        fixtures = sorted(os.listdir('main/fixtures'))
        excludes = []
        for fixture in fixtures:
            if fixture not in excludes:
                execute_from_command_line(['manage.py', 'loaddata', fixture])
