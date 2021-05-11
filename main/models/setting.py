from django.db.models import Model
from django.db.models import CharField

class Setting(Model):
    name = CharField(max_length=200, verbose_name='Название')
    slug = CharField(max_length=200, verbose_name='slug')
    value = CharField(max_length=200, verbose_name='Значение')

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return self.name

    @staticmethod
    def convert_value(value):
        # Проверка на натуральное числовое значение
        if value.isdigit():
            return int(value)

        # Проверка на действительное числовое значение
        try:
            return float(value)
        except ValueError:
            pass

        # Проверка на двоичное значение
        yes_list = ['да', 'yes', 'true']
        no_list = ['нет', 'yes', 'false']
        value_lower = value.lower()
        if value_lower in yes_list:
            return True
        elif value_lower in no_list:
            return False

        # Возвращаем любое прочее строковое значение
        return value

    @staticmethod
    def get(slug):
        # Проверяем не список ли якорей
        if isinstance(slug, list):
            # Список
            settings = Setting.objects.filter(slug__in=slug)
            values = { setting.slug: Setting.convert_value(setting.value) for setting in settings }
            return values
        else:
            # Один якорь
            value = Setting.objects.get(slug=slug).value
            return Setting.convert_value(value)