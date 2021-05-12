from django.db.models import Model
from django.db.models import CASCADE, SET_NULL
from django.db.models import ForeignKey, CharField, IntegerField
from django.db.models import F
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

# Функция получения порядкового номера по умолчанию
def get_default_order():
  return Menu.objects.all().count() + 1

class Menu(Model):
    name = CharField(max_length=200, verbose_name='Название')
    parent = ForeignKey('Menu', null=True, blank=True, default=None, on_delete=CASCADE, verbose_name='Родительский пункт')
    order = IntegerField(default=get_default_order, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        # ordering = ['order']

    def __str__(self):
        return self.name

    def order_up(self):
        childs = self.childs
        childs_count = len(childs)
        higher = self.higher
        if higher:
            higher_childs = higher.childs
            higher_childs_count = len(higher_childs)

            higher.order += childs_count + 1
            higher.save()

            if higher_childs:
                higher_childs.update(order=F('order') + childs_count + 1)
        else:
            higher_childs_count = 0

        self.order -= higher_childs_count + 1
        self.save()
        childs.update(order=F('order')-higher_childs_count-1)

    def order_down(self):
        childs = self.childs
        childs_count = len(childs)
        lower = self.lower
        if lower:
            lower_childs = lower.childs
            lower_childs_count = len(lower_childs)

            lower.order -= childs_count + 1
            lower.save()

            if lower_childs:
                lower_childs.update(order=F('order') - childs_count - 1)
        else:
            lower_childs_count = 0

        self.order += lower_childs_count + 1
        self.save()
        childs.update(order=F('order')+lower_childs_count+1)

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

# Функция для рекурсии
def _admin_str(obj, name):
    if not obj.parent:
        return name
    return '|____' + _admin_str(obj.parent, name)

# Функция рекурсии для получения всех подпунктов
def _childs_all(childs):
    for child in childs:
        childs += _childs_all(list(child.childs))
    return childs

# Сигналы --------------------------------------------------------------------------------------------------------------

# Удаление объекта
@receiver(pre_delete, sender=Menu)
def address_pre_delete(sender, instance, using, **kwargs):
    childs_count = instance.childs_count
    lowers = instance.lower_order
    lowers.update(order=F('order')-childs_count-1)

# Создание и изменение объекта
@receiver(pre_save, sender=Menu)
def address_pre_save(sender, instance, raw, using, update_fields, **kwargs):
    if not instance.pk:
        parent = instance.parent
        if parent:
            print(parent.childs_all)

            child_last = parent.childs_last
            instance.order = child_last.order + 1
            child_last.lower_order.update(order=F('order')+1)
        return False

    try:
        old_parent = Menu.objects.get(pk=instance.pk).parent
    except Menu.DoesNotExist:
        return False

    # if not old_parent == instance.parent:
    #     childs_count = instance.childs_count
    #     lowers = instance.lower_order
    #     lowers.update(order=F('order') - childs_count - 1)
    #
    #     parent = instance.parent
    #     if parent:
    #         child_last = Menu.objects.filter(parent=instance.parent).order_by('order').last()
    #         instance.order = child_last.order + 1
    #         child_last.lower_order.update(order=F('order') + 1)

        # childs = Menu.objects.filter(parent=instance.parent).order_by('order')
        # if parent:
        #     pass
