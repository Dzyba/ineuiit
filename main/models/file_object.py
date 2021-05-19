from django.db.models import Model
from django.db.models import CharField, ForeignKey, FileField
from django.db.models import SET_NULL
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class FileObject(Model):
    name = CharField(max_length=200, verbose_name='Название')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    menu = ForeignKey('Menu', blank=True, null=True, on_delete=SET_NULL, verbose_name='Меню')
    object = FileField(upload_to='main/file_objects/', verbose_name='Файл')

    def __str__(self):
        return '%s -> %s' % (self.menu if self.menu else '|', self.name)

    @staticmethod
    def get_menu(menu):
        file_objects = FileObject.objects.filter(menu=menu)
        return {file_object.slug: file_object.name for file_object in file_objects}

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

# Сигналы --------------------------------------------------------------------------------------------------------------

# Удаление файла при удалении объекта
@receiver(pre_delete, sender=FileObject)
def object_pre_delete(sender, instance, using, **kwargs):
    instance.object.delete(save=False)

# Удаление файла при изменении объекта
@receiver(pre_save, sender=FileObject)
def object_pre_save(sender, instance, raw, using, update_fields, **kwargs):

    if not instance.pk:
        return False

    try:
        old_object = FileObject.objects.get(pk=instance.pk).object
    except FileObject.DoesNotExist:
        return False

    if not old_object == instance.object:
        old_object.delete(save=False)