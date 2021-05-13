from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'INEUIIT'
admin.site.site_title = 'INEUIIT'
urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)