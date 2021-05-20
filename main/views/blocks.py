from django.template.loader import render_to_string
from main.models import Direction

class Blocks:
    @staticmethod
    def block_directions_p():
        context = {
            'directions': Direction.objects.all()
        }
        return render_to_string('main/edupix/_block_directions.html', context)