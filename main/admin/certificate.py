from django.contrib import admin
from main.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ['name']