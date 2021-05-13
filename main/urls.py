from django.urls import path, register_converter
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from main.views import *

app_name = 'main'
urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index')
]