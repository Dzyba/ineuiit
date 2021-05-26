from django.contrib import admin
from main.models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    ordering = ['-datetime']
    list_display = ('datetime', 'name', 'slug', 'image', 'description')
    list_display_links = ['datetime', 'name']
