from django.db.models import Model
from django.db.models import CASCADE, SET_NULL
from django.db.models import ForeignKey, CharField, IntegerField, TextChoices
from django.db.models import F
from django.db.models.signals import pre_delete, pre_save, post_delete, post_save
from django.dispatch import receiver
from .page import Page
from .cathedra import Cathedra
from .inner_link import InnerLink

from .file_object import FileObject

# Функция получения порядкового номера по умолчанию
def get_default_order():
  return Menu.objects.all().count() + 1

class Menu(Model):
    class Kind(TextChoices):
        DEFAULT = 'default', '-'
        INDEX = 'index', 'Главная'
        GROUP = 'group', 'Группа (без страницы)'
        GROUP_PAGE = 'group_page', 'Группа (co страницей)'
        PAGE = 'page', 'Страница'
        FILEOBJECT = 'fileobject', 'Ссылка на файл'
        SCHEDULE = 'schedule', 'Расписание'
        STAFF_ITEM = 'staff_item', 'Сотрудник'
        CATHEDRA_LIST = 'cathedra_list', 'Список кафедр'
        CATHEDRA_ITEM = 'cathedra_item', 'Кафедра'
        DIRECTION_ITEM = 'direction_item', 'Направление'
        INNER_LINK = 'inner_link', 'Внутренняя ссылка'

        @staticmethod
        def get_list():
            return [kind.label for kind in Menu.Kind]

        @staticmethod
        def get_choice_list():
            return [[kind.value, kind.label] for kind in Menu.Kind]

    name = CharField(max_length=200, verbose_name='Название')
    parent = ForeignKey('Menu', null=True, blank=True, default=None, on_delete=CASCADE, verbose_name='Родительский пункт')
    kind = CharField(choices=Kind.choices, max_length=20, default=Kind.DEFAULT, verbose_name='Тип')
    order = IntegerField(default=get_default_order, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        # ordering = ['order']

    def __str__(self):
        return self.name

    def order_up(self):
        childs_all = self.childs_all
        childs_all_count = len(childs_all)
        higher = self.higher
        if higher:
            higher_childs_all = higher.childs_all
            higher_childs_all_count = len(higher_childs_all)

            higher.order += childs_all_count + 1
            higher.save()

            if higher_childs_all:
                higher_childs_all.update(order=F('order') + childs_all_count + 1)
        else:
            higher_childs_all_count = 0

        self.order -= higher_childs_all_count + 1
        self.save()
        childs_all.update(order=F('order')-higher_childs_all_count-1)

    def order_down(self):
        childs_all = self.childs_all
        childs_all_count = len(childs_all)
        lower = self.lower
        if lower:
            lower_childs_all = lower.childs_all
            lower_childs_all_count = len(lower_childs_all)

            lower.order -= childs_all_count + 1
            lower.save()

            if lower_childs_all:
                lower_childs_all.update(order=F('order') - childs_all_count - 1)
        else:
            lower_childs_all_count = 0

        self.order += lower_childs_all_count + 1
        self.save()
        childs_all.update(order=F('order')+lower_childs_all_count+1)

    @property
    def level(self):
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
    level.fget.short_description = 'Название'

    @property
    def order_delta_parent(self):
        return self.order - self.parent.order
    order_delta_parent.fget.short_description = 'Разница порядка с родителем'

    @property
    def order_in_parent(self):
        return Menu.objects.filter(parent=self.parent, order__lt=self.order).count() + 1
    order_in_parent.fget.short_description = 'Порядок в родителе'

    @property
    def order_in_parent_is_first(self):
        return bool(self.order_in_parent == 1)
    order_in_parent.fget.short_description = 'Порядок в родителе, первый'

    @property
    def order_in_parent_is_last(self):
        return bool(self.order_in_parent == self.siblings_count)
    order_in_parent.fget.short_description = 'Порядок в родителе, последний'

    @property
    def higher(self):
        return self.siblings.filter(order__lt=self.order).order_by('order').last()
    higher.fget.short_description = 'Пункт выше на один'

    @property
    def higher_order(self):
        return Menu.objects.filter(order__lt=self.order).order_by('order')
    higher_order.fget.short_description = 'Более высокие пункты'

    @property
    def lower(self):
        return self.siblings.filter(order__gt=self.order).order_by('order').first()
    lower.fget.short_description = 'Пункт ниже на один'

    @property
    def lower_order(self):
        return Menu.objects.filter(order__gt=self.order).order_by('order')
    lower_order.fget.short_description = 'Более низкие пункты'

    @property
    def siblings(self, exclude=False):
        if exclude:
            Menu.objects.filter(parent=self.parent).exclude(id=self.id).order_by('order')
        else:
            return Menu.objects.filter(parent=self.parent).order_by('order')
    siblings.fget.short_description = 'Одноуровневые пункты'

    @property
    def siblings_count(self, exclude=False):
        if exclude:
            Menu.objects.filter(parent=self.parent).exclude(id=self.id).count()
        else:
            return Menu.objects.filter(parent=self.parent).count()
    siblings.fget.short_description = 'Одноуровневые пункты, количество'

    @property
    def childs(self):
        return Menu.objects.filter(parent=self).order_by('order')
    childs.fget.short_description = 'Подпункты'

    @property
    def childs_all(self):
        return _childs_all(self.childs)
    childs_all.fget.short_description = 'Подпункты, все'

    @property
    def childs_all_last(self):
        childs_all = self.childs_all
        return _childs_all(self.childs).last() if childs_all else None
    childs_all.fget.short_description = 'Подпункты, все, последний'

    @property
    def childs_all_count(self):
        return _childs_all(self.childs).count()
    childs_all_count.fget.short_description = 'Подпункты, все, количество'

    @property
    def childs_last(self):
        return Menu.objects.filter(parent=self).order_by('order').last()
    childs_last.fget.short_description = 'Подпункты, последний'

    @property
    def childs_count(self):
        return Menu.objects.filter(parent=self).count()
    childs_count.fget.short_description = 'Подпункты, количество'

    @property
    def admin_str(self):
        return _admin_str(self, self.name)
    admin_str.fget.short_description = 'Дерево'

    @property
    def url(self):
        if self.kind == Menu.Kind.INDEX:
            return '/'
        elif self.kind == Menu.Kind.PAGE or self.kind == Menu.Kind.GROUP_PAGE:
            try:
                return '/' + Page.objects.get(menu=self).slug
            except:
                pass
        elif self.kind == Menu.Kind.FILEOBJECT:
            return FileObject.objects.get(menu=self).object.path
        elif self.kind == Menu.Kind.SCHEDULE:
            return '/schedule'
        elif self.kind == Menu.Kind.CATHEDRA_LIST:
            return '/cathedras'
        elif self.kind == Menu.Kind.CATHEDRA_ITEM:
            return '/cathedra/'
        elif self.kind == Menu.Kind.STAFF_ITEM:
            return '/staff/'
        elif self.kind == Menu.Kind.DIRECTION_ITEM:
            return '/direction/'
        elif self.kind == Menu.Kind.INNER_LINK:
            parent_url = self.parent.url if self.parent else ''
            inner_link = InnerLink.objects.get(menu=self).slug
            return '%s%s' % (parent_url, inner_link)

        return 'javascript:void(0);'

    admin_str.fget.short_description = 'Дерево'

    @staticmethod
    def reorder(exclude_ids=[]):
        menus = Menu.objects.all().exclude(id__in=exclude_ids).order_by('order')
        i = 1
        for menu in menus:
            menu.order = i
            menu.save()
            i += 1

    @staticmethod
    def get_dict():
        menu_0 = Menu.objects.filter(kind=Menu.Kind.INDEX).first()
        menus = {
            'menu': menu_0,
            'childs': []
        }

        menus_1 = menu_0.childs
        for menu_1 in menus_1:
            items, is_childs = menu_1._get_menu_dict_items()
            for item in items:
                menus['childs'].append(item)

            if is_childs:
                menus_2 = menu_1.childs
                for menu_2 in menus_2:
                    items, is_childs = menu_2._get_menu_dict_items()
                    for item in items:
                        menus['childs'][-1]['childs'].append(item)

                    if is_childs:
                        menus_3 = menu_2.childs
                        for menu_3 in menus_3:
                            items, is_childs = menu_3._get_menu_dict_items()
                            for item in items:
                                menus['childs'][-1]['childs'][-1]['childs'].append(item)

        return menus

    def _get_menu_dict_items(self):
        is_childs = True
        if self.kind == Menu.Kind.CATHEDRA_ITEM:
            cathedras = Cathedra.objects.all()
            inner_links =  InnerLink.objects.filter(menu__parent=self)
            items = [{
                    'menu': { 'name': cathedra.name },
                    'url':self.url + cathedra.slug,
                    'childs': [
                        {
                            'menu': {
                                'name': link.name
                            },
                            'url': self.url + cathedra.slug + link.slug,
                            'childs': []
                        }
                    for link in inner_links]
                } for cathedra in cathedras]

            is_childs = False
        elif self.kind == Menu.Kind.STAFF_ITEM:
            items = [{'menu': self, 'url':self.url, 'childs': []}] # TODO
        else:
            items = [{'menu': self, 'url':self.url, 'childs': []}]


        return items, is_childs

# Функция для рекурсии
def _admin_str(obj, name):
    if not obj.parent:
        return name
    return '|____' + _admin_str(obj.parent, name)

# Функция рекурсии для получения всех подпунктов
def _childs_all(childs):
    for child in childs:
        childs = childs | _childs_all(child.childs)
    return childs

# Сигналы --------------------------------------------------------------------------------------------------------------

# Вспомогательная функция добавления в дерево
def _add_menu(instance):
    parent = instance.parent
    if parent:
        child_all_last = parent.childs_all_last
        if child_all_last:
            instance.order = child_all_last.order + 1
            child_all_last.lower_order.update(order=F('order') + 1)
        else:
            instance.order = parent.order + 1
            parent.lower_order.update(order=F('order') + 1)
    return False

# Удаление объекта
@receiver(post_delete, sender=Menu)
def menu_post_delete(sender, instance, using, **kwargs):
    Menu.reorder()

# Создание и изменение объекта
@receiver(pre_save, sender=Menu)
def menu_pre_save(sender, instance, raw, using, update_fields, **kwargs):
    # Добавление
    if not instance.pk:
        return _add_menu(instance)

    # Изменение
    try:
        old_parent = Menu.objects.get(pk=instance.pk).parent
    except Menu.DoesNotExist:
        return False

    # Порядок меняется, если поменялся родитель
    if not old_parent == instance.parent:
        childs_all = instance.childs_all
        childs_all_include = childs_all | Menu.objects.filter(id=instance.id)

        parent = instance.parent
        instance_order = instance.order
        if not parent:
            base_order = Menu.objects.all().order_by('order').last().order

            Menu.objects.filter(id=instance.id).update(order=base_order + 1)
            childs_all.update(order=base_order + F('order') - instance_order + 1)
            Menu.reorder()

            instance.order = Menu.objects.filter(id=instance.id)[0].order

        else:
            childs_all_include_ids = [child.id for child in childs_all_include]
            childs_all_include_count = len(childs_all_include_ids)
            # last_order = childs_all_include.last().order # instance_order - first_order

            parent_childs_all_last = parent.childs_all_last
            if parent_childs_all_last:
                base_order = parent_childs_all_last.order
                lowers = parent_childs_all_last.lower_order.exclude(id__in=childs_all_include_ids)
            else:
                base_order = parent.order
                lowers = parent.lower_order.exclude(id__in=childs_all_include_ids)

            lowers.update(order=F('order') + childs_all_include_count)
            childs_all_include.update(order=base_order + F('order') - instance_order + 1)
            Menu.reorder()

            instance.order = Menu.objects.filter(id=instance.id)[0].order