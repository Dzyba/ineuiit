from django.db.models import Model
from django.db.models import CharField, TextField, ForeignKey, BooleanField, ImageField
from django.db.models import SET_NULL
from .setting import Setting
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class Page(Model):
    name = CharField(max_length=200, verbose_name='Название')

    is_sidebar = BooleanField(default=False, verbose_name='Сайдбар?')
    sidebar_name = CharField(max_length=200, null=True, blank=True, default='', verbose_name='Сайдбар, название')
    # sidebar_menu = ForeignKey('Menu', blank=True, null=True, on_delete=SET_NULL, verbose_name='Сайдбар, пункт меню')

    slug = CharField(max_length=200, verbose_name='Техническое имя')
    menu = ForeignKey('Menu', blank=True, null=True, on_delete=SET_NULL, verbose_name='Меню')
    html = TextField(verbose_name='HTML')

    def __str__(self):
        return '%s -> %s' % (self.menu if self.menu else '|', self.name)

    @staticmethod
    def get(slug):
        try:
            text = Page.objects.get(slug=slug).html
        except:
            text = Setting.get('no_page_parent')
        return text

    @staticmethod
    def get_menu(menu):
        pages = Page.objects.filter(menu=menu)
        return {page.slug: page.name for page in pages}

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

class PageImage(Model):
    page = ForeignKey(Page, null=True, blank=True, on_delete=SET_NULL, verbose_name='Картинка для страницы')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    image = ImageField(upload_to='main/images/page_image/images', null=True, blank=True, verbose_name='Картинка')

    def __str__(self):
        return self.image.page.name

    class Meta:
        verbose_name = 'Картинка для страницы'
        verbose_name_plural = 'Картинки для страниц'

# Сигналы --------------------------------------------------------------------------------------------------------------

# Удаление картинки при удалении объекта
@receiver(pre_delete, sender=PageImage)
def page_image_pre_delete(sender, instance, using, **kwargs):
    instance.image.delete(save=False)

# Удаление картинки при изменении объекта
@receiver(pre_save, sender=PageImage)
def page_image_pre_save(sender, instance, raw, using, update_fields, **kwargs):

    if not instance.pk:
        return False

    try:
        old_image = PageImage.objects.get(pk=instance.pk).image
    except PageImage.DoesNotExist:
        return False

    if not old_image == instance.image:
        old_image.delete(save=False)