from django.db.models import Model
from django.db.models import CharField, TextField, BooleanField, ImageField, DateTimeField
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class News(Model):
    name = CharField(max_length=200, verbose_name='Заголовок')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    image = ImageField(upload_to='main/images/news/images', null=True, blank=True, verbose_name='Картинка')
    description = CharField(max_length=1000, null=True, blank=True, verbose_name='Описание')
    html = TextField(verbose_name='HTML')
    datetime = DateTimeField(verbose_name='Дата и время')
    is_slider = BooleanField(default=False, verbose_name='Слайдер?')

    def __str__(self):
        return self.name

    @property
    def url(self):
        return '/news_item/' + self.slug

    @staticmethod
    def get(slug):
        return News.objects.get(slug=slug)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

# Сигналы --------------------------------------------------------------------------------------------------------------

# Удаление картинки при удалении объекта
@receiver(pre_delete, sender=News)
def news_pre_delete(sender, instance, using, **kwargs):
    instance.icon.delete(save=False)
    instance.image.delete(save=False)

# Удаление картинки при изменении объекта
@receiver(pre_save, sender=News)
def news_pre_save(sender, instance, raw, using, update_fields, **kwargs):

    if not instance.pk:
        return False

    try:
        old_image = News.objects.get(pk=instance.pk).image
    except News.DoesNotExist:
        return False

    if not old_image == instance.image:
        old_image.delete(save=False)