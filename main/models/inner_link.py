from django.db.models import Model
from django.db.models import CharField, ForeignKey
from django.db.models import SET_NULL


class InnerLink(Model):
    name = CharField(max_length=200, verbose_name='Название')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    menu = ForeignKey('Menu', blank=True, null=True, on_delete=SET_NULL, verbose_name='Меню')

    def __str__(self):
        return '%s -> %s' % (self.menu if self.menu else '|', self.name)

    @staticmethod
    def get_menu(menu):
        inner_links = InnerLink.objects.filter(menu=menu)
        return {inner_link.slug: inner_link.name for inner_link in inner_links}

    class Meta:
        verbose_name = 'Внутренняя ссылка'
        verbose_name_plural = 'Внутренние ссылки'