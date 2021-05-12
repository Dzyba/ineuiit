from django.db.models import Model
from django.db.models import CharField, TextField
from .setting import Setting


class Page(Model):
    name = CharField(max_length=200, verbose_name='Название')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    menu = CharField(max_length=200, verbose_name='Пункт меню')
    html = TextField(verbose_name='HTML')

    def __str__(self):
        return '%s -> %s' % (self.menu, self.name)

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
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'