from django.forms import Form, ModelChoiceField, CharField, TextInput, Select, EmailField, EmailInput
from main.models import ScheduleGroup, Certificate

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
    email = EmailField(
        required=True,
        widget=EmailInput(
            attrs={
                'class': '',
                'placeholder': 'Email'
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
    certificate = ModelChoiceField(
        queryset=Certificate.objects.all(),
        required=True,
        widget=Select(
            attrs={
                'class': ''
            }
        )
    )
    # certificate = CharField(
    #     max_length=1000,
    #     required=True,
    #     widget=TextInput(
    #         attrs={
    #             'class': '',
    #             'maxlength': 1000,
    #             'placeholder': 'Необходимая справка'
    #         }
    #     )
    # )