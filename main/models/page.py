from django.db.models import Model
from django.db.models import CharField, TextField, ForeignKey, BooleanField
from django.db.models import SET_NULL
from .setting import Setting


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