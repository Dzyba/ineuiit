from django.db.models import Model
from django.db.models import CharField


class Certificate(Model):
    name = CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'