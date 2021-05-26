from django.urls import path, register_converter, include
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
    path('schedule', ScheduleView.as_view(), name='schedules'),
    path('schedule/<slug:slug>', ScheduleView.as_view(), name='schedule'),

    path('news', NewsView.as_view(), name='news'),
    path('news/<int:page>', NewsView.as_view(), name='news-page'),
    path('news_item/<slug:slug>', NewsItemView.as_view(), name='news-item'),

    path('announcements', AnnouncementsView.as_view(), name='announcements'),
    path('announcements/<int:page>', AnnouncementsView.as_view(), name='announcements-page'),
    path('announcement/<slug:slug>', AnnouncementsItemView.as_view(), name='announcements-item'),

    path('certificates', CertificatesView.as_view(), name='certificates'),

    path('send_push', send_push),

    path('<slug:slug>', PageView.as_view(), name='page'),
]