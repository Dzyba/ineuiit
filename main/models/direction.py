from django.db.models import Model
from django.db.models import CharField, TextField, ImageField, ForeignKey, TextChoices, CASCADE
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class Direction(Model):
    class Degree(TextChoices):
        MAGISTRACY = 'magistracy', 'Магистратура'
        BACCALAUREATE = 'baccalaureate', 'Бакалавриат'

        @staticmethod
        def get_list():
            return [degree.label for degree in Direction.Degree]

        @staticmethod
        def get_choice_list():
            return [[degree.value, degree.label] for degree in Direction.Degree]

    name = CharField(max_length=200, verbose_name='Название')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    degree = CharField(choices=Degree.choices, max_length=20, default=Degree.MAGISTRACY, verbose_name='Степень')
    image = ImageField(upload_to='main/images/directions/images', null=True, blank=True, verbose_name='Картинка')
    html = TextField(verbose_name='HTML')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

class Exam(Model):
    name = CharField(max_length=200, verbose_name='Название')
    score = CharField(max_length=200, verbose_name='Балл')
    direction = ForeignKey(Direction, on_delete=CASCADE, verbose_name='Направление')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Экзамен'
        verbose_name_plural = 'Экзамены'

# Сигналы --------------------------------------------------------------------------------------------------------------

# Удаление картинки при удалении объекта
@receiver(pre_delete, sender=Direction)
def direction_pre_delete(sender, instance, using, **kwargs):
    instance.icon.delete(save=False)
    instance.image.delete(save=False)

# Удаление картинки при изменении объекта
@receiver(pre_save, sender=Direction)
def direction_pre_save(sender, instance, raw, using, update_fields, **kwargs):

    if not instance.pk:
        return False

    try:
        old_image = Direction.objects.get(pk=instance.pk).image
    except Direction.DoesNotExist:
        return False

    if not old_image == instance.image:
        old_image.delete(save=False)