from django.template.loader import render_to_string
from main.models import Direction, Staff

class Blocks:
    @staticmethod
    def block_directions_p():
        context = {'directions': Direction.objects.all()}
        return render_to_string('main/edupix/_block_directions_p.html', context)

    @staticmethod
    def block_directions_table():
        context = {'directions': Direction.objects.all()}
        return render_to_string('main/edupix/_block_directions_table.html', context)

    @staticmethod
    def block_staff_table(categories=None):
        context = {'staff': Staff.objects.filter(category__in=categories)}
        return render_to_string('main/edupix/_block_staff_table.html', context)