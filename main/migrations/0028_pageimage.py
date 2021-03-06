# Generated by Django 3.2 on 2021-05-21 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_menu_is_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='main/images/page_image/images', verbose_name='Картинка')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.page', verbose_name='Картинка для страницы')),
            ],
            options={
                'verbose_name': 'Картинка для страницы',
                'verbose_name_plural': 'Картинки для страниц',
            },
        ),
    ]
