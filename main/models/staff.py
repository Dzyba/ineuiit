from django.db.models import Model
from django.db.models import CharField, ForeignKey, ImageField, TextField, TextChoices
from django.db.models import SET_NULL
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class Staff(Model):
    class Category(TextChoices):
        STAFF = 'staff', 'Штатный'
        LEADER = 'leader', 'Руководитель'

        @staticmethod
        def get_list():
            return [category.label for category in Staff.Category]

        @staticmethod
        def get_choice_list():
            return [[category.value, category.label] for category in Staff.Category]

    name = CharField(max_length=200, verbose_name='Имя')
    position = CharField(max_length=200, verbose_name='Должность')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    cathedra = ForeignKey('Cathedra', null=True, blank=True, on_delete=SET_NULL, related_name='staff', verbose_name='Кафедра')
    category = CharField(choices=Category.choices, max_length=20, default=Category.STAFF, verbose_name='Категория')
    html = TextField(verbose_name='HTML')

    image = ImageField(upload_to='main/images/staff/images', null=True, blank=True, verbose_name='Картинка')

    def __str__(self):
        return '%s -> %s' % (self.cathedra if self.cathedra else '|', self.name)

    @property
    def url(self):
        return '/staff/' + self.slug

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

# Сигналы --------------------------------------------------------------------------------------------------------------

# Удаление картинки при удалении объекта
@receiver(pre_delete, sender=Staff)
def staff_pre_delete(sender, instance, using, **kwargs):
    instance.image.delete(save=False)

# Удаление картинки при изменении объекта
@receiver(pre_save, sender=Staff)
def staff_pre_save(sender, instance, raw, using, update_fields, **kwargs):

    if not instance.pk:
        return False

    try:
        old_image = Staff.objects.get(pk=instance.pk).image
    except Staff.DoesNotExist:
        return False

    if not old_image == instance.image:
        old_image.delete(save=False)