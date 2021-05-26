from django.forms import Form, ModelChoiceField, CharField, TextInput, Select
from main.models import ScheduleGroup

class CertificateOrderForm(Form):
    name = CharField(
        max_length=200,
        required=True,
        widget=TextInput(
            attrs={
                'class': '',
                'maxlength': 200,
                'placeholder': 'Фамилия и имя'
            }
        )
    )
    group = CharField(
        max_length=200,
        required=True,
        widget=TextInput(
            attrs={
                'class': '',
                'maxlength': 200,
                'placeholder': 'Группа'
            }
        )
    )
    certificate = CharField(
        max_length=1000,
        required=True,
        widget=TextInput(
            attrs={
                'class': '',
                'maxlength': 1000,
                'placeholder': 'Необходимая справка'
            }
        )
    )