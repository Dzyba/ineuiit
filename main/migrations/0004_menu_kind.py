# Generated by Django 3.2 on 2021-05-13 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210512_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='kind',
            field=models.CharField(choices=[('group', 'Группа (без страницы)'), ('group_page', 'Группа (co страницей)'), ('page', 'Страница')], default='group', max_length=20, verbose_name='Тип'),
        ),
    ]
