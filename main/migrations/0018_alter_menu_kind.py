# Generated by Django 3.2 on 2021-05-19 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='kind',
            field=models.CharField(choices=[('default', '-'), ('index', 'Главная'), ('group', 'Группа (без страницы)'), ('group_page', 'Группа (co страницей)'), ('page', 'Страница'), ('fileobject', 'Ссылка на файл'), ('schedule', 'Расписание'), ('staff_item', 'Сотрудник'), ('cathedra_list', 'Список кафедр'), ('cathedra_item', 'Кафедра'), ('direction_item', 'Направление'), ('inner_link', 'Внутренняя ссылка')], default='default', max_length=20, verbose_name='Тип'),
        ),
    ]