from django.db.models import Model
from django.db.models import CharField, ForeignKey, TextField, TextChoices, IntegerField, BooleanField
from django.db.models import SET_NULL, CASCADE
from .menu import Menu

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
        schedule_menu = Menu.objects.filter(kind=Menu.Kind.SCHEDULE).first()
        breadcrumbs.append({
            'name': schedule_menu.name,
            'url': schedule_menu.url
        })
        return breadcrumbs

    def get_schedule_dict(self):
        schedule = []
        days = self.days.all()
        for day in days:
            schedule.append({
                'day': day,
                **day.get_schedule_dict()
            })
        return schedule

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
    group = ForeignKey(ScheduleGroup, on_delete=CASCADE, related_name='days', verbose_name='Группа')

    def __str__(self):
        return str(self.group) + ' ' + str(self.day)

    def get_schedule_dict(self):
        timeslots = list(self.timeslots.all())
        schedule = {
            'rowspan': len(timeslots) + 1,
            'timeslots': timeslots
        }
        return schedule

    class Meta:
        ordering = ['group__name', 'day']
        verbose_name = 'Расписание - Учебный день'
        verbose_name_plural = 'Расписание - Учебные дни'

class ScheduleTimeSlot(Model):
    day = ForeignKey(ScheduleDay, on_delete=CASCADE, related_name='timeslots', verbose_name='Учебный день')
    number = IntegerField(verbose_name='Номер')
    time = CharField(max_length=50, verbose_name='Время начала - время конца')
    pair_numerator = CharField(max_length=200, null=True, blank=True, default=None, verbose_name='Пара (числитель)')
    pair_denominator = CharField(max_length=200, null=True, blank=True, default=None, verbose_name='Пара (знаменатель)')
    is_whole = BooleanField(default=True, verbose_name='Целый слот?')

    def __str__(self):
        return str(self.day) + ' ' + self.time + ' ' + (self.pair_numerator if self.pair_numerator else '-') + ' / ' + (self.pair_denominator if self.pair_denominator else '-')

    class Meta:
        ordering = ['day__group__name', 'day__day', 'number']
        verbose_name = 'Расписание - Временной слот'
        verbose_name_plural = 'Расписание - Временные слоты'
