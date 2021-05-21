from django.template.loader import render_to_string
from main.models import Direction

class Blocks:
    @staticmethod
    def block_directions_p():
        context = {'directions': Direction.objects.all()}
        return render_to_string('main/edupix/_block_directions_p.html', context)

    @staticmethod
    def block_directions_table():
        context = {'directions': Direction.objects.all()}
        return render_to_string('main/edupix/_block_directions_table.html', context)