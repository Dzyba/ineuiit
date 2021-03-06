# Generated by Django 3.2 on 2021-05-13 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_menu_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='kind',
            field=models.CharField(choices=[('default', '-'), ('group', 'Группа (без страницы)'), ('group_page', 'Группа (co страницей)'), ('page', 'Страница'), ('schedule', 'Расписание'), ('staff_list', 'Сотрудники'), ('staff_item', 'Сотрудник'), ('cathedra_list', 'Кафедры'), ('cathedra_item', 'Кафедра'), ('cathedra_page', 'Страница кафедры')], default='default', max_length=20, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='page',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.menu', verbose_name='Меню'),
        ),
    ]
