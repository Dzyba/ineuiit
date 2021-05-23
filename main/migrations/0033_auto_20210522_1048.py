# Generated by Django 3.2 on 2021-05-22 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20210521_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scheduleday',
            options={'ordering': ['group__name', 'day'], 'verbose_name': 'Расписание - Учебный день', 'verbose_name_plural': 'Расписание - Учебные дни'},
        ),
        migrations.AlterModelOptions(
            name='scheduletimeslot',
            options={'ordering': ['day__group__name', 'day__day', 'number'], 'verbose_name': 'Расписание - Временной слот', 'verbose_name_plural': 'Расписание - Временные слоты'},
        ),
        migrations.RemoveField(
            model_name='scheduleday',
            name='name',
        ),
        migrations.RemoveField(
            model_name='scheduleday',
            name='number',
        ),
        migrations.AddField(
            model_name='scheduleday',
            name='day',
            field=models.CharField(choices=[('1', 'Пн'), ('2', 'Вт'), ('3', 'Ср'), ('4', 'Чт'), ('5', 'Пт'), ('6', 'Сб'), ('7', 'Вс')], default='1', max_length=20, verbose_name='День'),
        ),
        migrations.AlterField(
            model_name='schedulegroup',
            name='message',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Важное сообщение'),
        ),
    ]