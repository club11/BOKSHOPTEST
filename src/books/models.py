from cProfile import label
from distutils.command.upload import upload
from email.policy import default
from locale import currency
from tabnanny import verbose
from django.db import models
from django.urls import reverse

from directories.models import Author, Serie, Genre ,Editor

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(
        verbose_name='название книги',
        max_length=100,
        blank=True,
    )
    picture = models.ImageField(
        verbose_name='картинка',
        upload_to = 'books/%Y/%m/%d/'           # указали куда upload ить
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=10,
        decimal_places=2
    )
    currency_price = models.CharField(
        verbose_name='валюта',
        max_length=4,
    )
    author = models.ForeignKey(
        Author,
         related_name='book_authors',
         on_delete=models.PROTECT,
         default=None
    )
    serie = models.ForeignKey(
        Serie,
         on_delete=models.PROTECT,
         related_name='book_series'
    )
    genre = models.ForeignKey(
        Genre,
         related_name='book_genres',
         on_delete=models.PROTECT,
         default=None
    )
    editor = models.ForeignKey(
        Editor,
         related_name='book_editors',
         on_delete=models.PROTECT,
         default=None
    )
    publishing_date = models.DateField(
        verbose_name='Год издания',
        blank=True
    )
    pages = models.IntegerField(
        verbose_name='количество страниц',
        blank=True,
    )
    binding = models.CharField(
        verbose_name='переплет',
        max_length=20,
        blank=True,
    )
    format = models.CharField(
        verbose_name='формат',
        max_length=20,
        blank=True,
    )    
    isbn = models.CharField(
        verbose_name='ISBN',
        max_length=20,
        blank=True,
    )    
    weigh = models.IntegerField(
        verbose_name='вес',
        blank=True,
    )
    age_restrictions = models.CharField(
        verbose_name='возрастные ограничения',
        max_length=20,
        blank=True,
    )   
    value_available = models.IntegerField(
        verbose_name='количество в наличии',
        blank=True,
    )
    available = models.BooleanField(
        verbose_name='доступен для заказа',
        default=None,
    )
    publication_date = models.DateTimeField(
        verbose_name='Дата внесения в каталог',
        auto_now=False,
        auto_now_add=True
    )
    publication_edit_date = models.DateTimeField(
        verbose_name='Дата последнего изменения карточки',
        auto_now=True,
        auto_now_add=False
    ) 


    def get_absolute_url(self):
        return reverse('books:book', args = [self.pk])

########################################################################################
#доработать рейтинг
#class RatingStar(models.Model):
#    value = models.IntegerField(
#        verbose_name="Значение",
#        default=0,
#    )
#
#    def __str__(self):
#        return f'{self.value}'
#
#    class Meta:
#        verbose_name = "Звезда рейтинга"    
#        verbose_name_plural = "Звезды рейтинга"  
#        ordering = ['-value']
#
#class Rating(models.Model):
#    customer_ip = models.CharField('IP адрес', max_length=15)
#    star = models.ForeignKey(
#        RatingStar,
#        on_delete=models.CASCADE,
#        verbose_name='звезда'
#    )
#    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='книга')
#
#    def __str__(self):
#        return f'{self.star}'
########################################################################################


        



    