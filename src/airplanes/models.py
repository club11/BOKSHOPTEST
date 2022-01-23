from tabnanny import verbose
from django.db import models

class SquareDim(models.Model):
    dim = models.CharField(
        verbose_name = "единица измерения площади",
        max_length = 100
    )

    def __str__(self) -> str:
        return self.dim

    class Meta:                                 # название таблицы - усицифировали и  множ числе
        verbose_name = "единица измерения"
        verbose_name_plural = "единицы измерений"

class Flat(models.Model):
    flat_number = models.IntegerField(          # КОМПОЗИЦИЯ - расширение функционала
        verbose_name = 'Номер квартиры')
    level = models.IntegerField(
        verbose_name = "Этаж")
    description = models.TextField(
        verbose_name = "Описание",
        blank = True,       # для пользователя, джанго приложение можно ли при приеме от пользователя данным быть незаполнеными
        null = True)         # для БД
    is_sold = models.BooleanField(
        verbose_name = 'Продана',
        default = False)
    lux = models.BooleanField(
        verbose_name = 'Люкс',
        default = False
    )
    created = models.DateTimeField(
        verbose_name = 'Дата внесения в базу данных',
        auto_now = False,        # редактирование даты обновление     
        auto_now_add = True)   #при создании
    updated = models.DateTimeField(
        verbose_name = "Дата последнего редактирования в БД",
        auto_now = True,       # редактирование даты обновление 
        auto_now_add = False     #при создании
    )
    square = models.IntegerField(
        verbose_name = "Площадь квартиры")
    square_dim = models.ForeignKey(
        SquareDim,
        on_delete=models.PROTECT,           #models.PROTECT цикаво
        related_name='flats'
    )

    def __str__(self) -> str:
        return f'Квартира {self.flat_number}'       #как объект отображается при выводе -ведь метод str

    class Meta:                                 # название таблицы - усицифировали и  множ числе
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"


    

