from django.urls import path, register_converter
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from main.views import *

app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cathedras', CathedrasView.as_view(), name='cathedras'),
    path('cathedra/<slug:slug>', CathedraView.as_view(), name='cathedra'),
    path('staff/<slug:slug>', StaffView.as_view(), name='staff'),
    path('direction/<slug:slug>', DirectionView.as_view(), name='direction'),
    path('<slug:slug>', PageView.as_view(), name='page')
]