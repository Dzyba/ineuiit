# Generated by Django 3.2 on 2021-05-19 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_menu_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='slug',
            field=models.CharField(default='', max_length=200, verbose_name='Техническое имя'),
            preserve_default=False,
        ),
    ]
