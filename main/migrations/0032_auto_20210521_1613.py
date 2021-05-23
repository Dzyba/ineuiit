# Generated by Django 3.2 on 2021-05-21 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_auto_20210521_1605'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scheduleday',
            options={'ordering': ['group__name', 'number'], 'verbose_name': 'Расписание - Учебный день', 'verbose_name_plural': 'Расписание - Учебные дни'},
        ),
        migrations.AlterModelOptions(
            name='schedulegroup',
            options={'ordering': ['name'], 'verbose_name': 'Расписание - Группа', 'verbose_name_plural': 'Расписание - Группы'},
        ),
        migrations.AlterModelOptions(
            name='scheduletimeslot',
            options={'ordering': ['day__group__name', 'day__number', 'number'], 'verbose_name': 'Расписание - Временной слот', 'verbose_name_plural': 'Расписание - Временные слоты'},
        ),
    ]