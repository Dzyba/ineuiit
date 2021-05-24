from django.forms import Form, ModelChoiceField, HiddenInput, CharField
from main.models import ScheduleGroup

class AdminPushForm(Form):
    text = CharField(max_length=1000, required=True)
    path = CharField(max_length=200, required=True, widget=HiddenInput())