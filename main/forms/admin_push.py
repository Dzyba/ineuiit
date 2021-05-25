from django.forms import Form, ModelChoiceField, HiddenInput, CharField, TextInput
from main.models import ScheduleGroup

class AdminPushForm(Form):
    header = CharField(max_length=200, required=True, widget=TextInput(attrs={'size': 100}))
    text = CharField(max_length=1000, required=True, widget=TextInput(attrs={'size': 100}))
    path = CharField(max_length=200, required=True, widget=HiddenInput())