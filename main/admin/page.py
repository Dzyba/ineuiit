from django.contrib import admin
from main.models import Page, PageImage

class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 0
    fields = ['slug', 'page', 'image']

@admin.register(PageImage)
class PageImageAdmin(admin.ModelAdmin):
    ordering = ['page', 'slug']
    list_display = ('slug', 'page', 'image')
    list_display_links = ['slug']

class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    fields = ['name', 'slug', 'menu', 'html']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    ordering = ['menu__parent', 'menu__name', 'name']
    list_display = ('name', 'menu', 'slug')
    list_display_links = ['name']

    inlines = [PageImageInline]
