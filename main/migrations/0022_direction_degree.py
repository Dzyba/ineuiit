# Generated by Django 3.2 on 2021-05-19 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_exam_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='degree',
            field=models.CharField(choices=[('magistracy', 'Магистратура'), ('baccalaureate', 'Бакалавриат')], default='magistracy', max_length=20, verbose_name='Степень'),
        ),
    ]
