from django.db.models import Model
from django.db.models import CharField, ForeignKey, ImageField, TextField
from django.db.models import SET_NULL
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class Cathedra(Model):
    name = CharField(max_length=200, verbose_name='Название')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    html = TextField(verbose_name='HTML')

    icon = ImageField(upload_to='main/images/cathedras/icons', null=True, blank=True, verbose_name='Иконка')
    image = ImageField(upload_to='main/images/cathedras/images', null=True, blank=True, verbose_name='Картинка')

    def __str__(self):
        return self.name

    @staticmethod
    def get_menu(menu):
        inner_links = Cathedra.objects.filter(menu=menu)
        return {inner_link.slug: inner_link.name for inner_link in inner_links}

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'

# Сигналы --------------------------------------------------------------------------------------------------------------

# Удаление иконки и картинки при удалении объекта
@receiver(pre_delete, sender=Cathedra)
def cathedra_pre_delete(sender, instance, using, **kwargs):
    instance.icon.delete(save=False)
    instance.image.delete(save=False)

# Удаление иконки и картинки при изменении объекта
@receiver(pre_save, sender=Cathedra)
def cathedra_pre_save(sender, instance, raw, using, update_fields, **kwargs):

    if not instance.pk:
        return False

    try:
        old_icon = Cathedra.objects.get(pk=instance.pk).icon
    except Cathedra.DoesNotExist:
        return False
    try:
        old_image = Cathedra.objects.get(pk=instance.pk).image
    except Cathedra.DoesNotExist:
        return False

    if not old_icon == instance.icon:
        old_icon.delete(save=False)
    if not old_image == instance.image:
        old_image.delete(save=False)