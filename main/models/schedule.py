from django.db.models import Model
from django.db.models import CharField, ForeignKey, TextField, TextChoices, IntegerField
from django.db.models import SET_NULL, CASCADE


class ScheduleGroup(Model):
    name = CharField(max_length=200, verbose_name='Название')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    message = TextField(default=None, null=True, blank=True, verbose_name='Важное сообщение')

    def __str__(self):
        return self.name

    @property
    def url(self):
        return '/schedule/' + self.slug

    def get_breadcrumbs_dict(self, menu):
        breadcrumbs = menu.get_breadcrumbs_dict()
        # breadcrumbs.append({
        #     'name': self.cathedra.name,
        #     'url': '/cathedra/' + self.cathedra.slug
        # })

        return breadcrumbs

    def get_schedule_dict(self):
        return None

    class Meta:
        ordering = ['name']
        verbose_name = 'Расписание - Группа'
        verbose_name_plural = 'Расписание - Группы'

class ScheduleDay(Model):
    class Day(TextChoices):
        MONDAY = '1', 'Пн'
        TUESDAY = '2', 'Вт'
        WEDNESDAY = '3', 'Ср'
        THURSDAY = '4', 'Чт'
        FRIDAY = '5', 'Пт'
        SATURDAY = '6', 'Сб'
        SUNDAY = '7', 'Вс'

        @staticmethod
        def get_list():
            return [day.label for day in ScheduleDay.Day]

        @staticmethod
        def get_choice_list():
            return [[day.value, day.label] for day in ScheduleDay.Day]

    day = CharField(choices=Day.choices, max_length=20, default=Day.MONDAY, verbose_name='День')
    group = ForeignKey(ScheduleGroup, on_delete=CASCADE, verbose_name='Группа')

    def __str__(self):
        return str(self.group) + ' ' + str(self.day)

    class Meta:
        ordering = ['group__name', 'day']
        verbose_name = 'Расписание - Учебный день'
        verbose_name_plural = 'Расписание - Учебные дни'

class ScheduleTimeSlot(Model):
    class Appearance(TextChoices):
        ALWAYS = 'always', 'Всегда'
        NUMERATOR = 'numerator', 'Числитель'
        DENOMINATOR = 'denominator', 'Знаменатель'

        @staticmethod
        def get_list():
            return [appearance.label for appearance in ScheduleTimeSlot.Appearance]

        @staticmethod
        def get_choice_list():
            return [[appearance.value, appearance.label] for appearance in ScheduleTimeSlot.Appearance]

    day = ForeignKey(ScheduleDay, on_delete=CASCADE, verbose_name='Учебный день')
    number = IntegerField(verbose_name='Номер')
    time = CharField(max_length=50, verbose_name='Время начала - время конца')
    pair = CharField(max_length=200, verbose_name='Пара')
    appearance = CharField(choices=Appearance.choices, max_length=20, default=Appearance.ALWAYS, verbose_name='Числитель/знаменатель')

    def __str__(self):
        return str(self.day) + ' ' + self.time + ' ' + self.pair

    class Meta:
        ordering = ['day__group__name', 'day__day', 'number']
        verbose_name = 'Расписание - Временной слот'
        verbose_name_plural = 'Расписание - Временные слоты'
