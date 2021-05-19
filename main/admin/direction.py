from django.contrib import admin
from main.models import Direction, Exam


class ExamInline(admin.TabularInline):
    model = Exam
    extra = 0
    fields = ['name', 'score', 'direction']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('name', 'score', 'direction')
    list_display_links = ['name']

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name', 'slug', 'degree', 'image')
    list_display_links = ['name']

    inlines=[ExamInline]