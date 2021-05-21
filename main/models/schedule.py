from django.db.models import Model
from django.db.models import CharField, ForeignKey, TextField, TextChoices, IntegerField
from django.db.models import SET_NULL, CASCADE


class ScheduleGroup(Model):
    name = CharField(max_length=200, verbose_name='Название')
    slug = CharField(max_length=200, verbose_name='Техническое имя')
    message = TextField(null=True, blank=True, verbose_name='Важное сообщение')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Расписание - Группа'
        verbose_name_plural = 'Расписание - Группы'

class ScheduleDay(Model):
    number = IntegerField(verbose_name='Номер')
    name = CharField(max_length=200, verbose_name='Название')
    group = ForeignKey(ScheduleGroup, on_delete=CASCADE, verbose_name='Группа')

    def __str__(self):
        return str(self.group) + ' ' + self.name

    class Meta:
        ordering = ['group__name', 'number']
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
        ordering = ['day__group__name', 'day__number', 'number']
        verbose_name = 'Расписание - Временной слот'
        verbose_name_plural = 'Расписание - Временные слоты'
