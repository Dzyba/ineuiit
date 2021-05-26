from django.contrib import admin
from main.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    ordering = ['-datetime']
    list_display = ('datetime', 'name', 'slug', 'image', 'description', 'is_slider')
    list_display_links = ['datetime', 'name']
