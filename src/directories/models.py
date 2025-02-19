from tabnanny import verbose
from django.db import models

from django.urls import reverse

# Create your models here.


class Author(models.Model):
    author = models.CharField(
        verbose_name='Автор',
        max_length=30)

    class Meta:
        verbose_name = "Автор",
        verbose_name_plural = "Авторы" 

    def __str__(self) -> str:
        return self.author

    def get_absolute_url(self):
        #return reverse('author', args=[self.pk])
        return reverse('directories:author_list')
class Serie(models.Model):
    serie = models.CharField(
        verbose_name='Серия',
        max_length=30)

    class Meta:
        verbose_name = "Серия",
        verbose_name_plural = "Серии" 

    def __str__(self) -> str:
        return self.serie
    
    def get_absolute_url(self):
        return reverse('directories:series_list')

class Genre(models.Model):
    genre = models.CharField(
        verbose_name='Жанр',
        max_length=30)

    class Meta:
        verbose_name = "Жанр",
        verbose_name_plural = "Жанры" 

    def __str__(self) -> str:
        return self.genre

    def get_absolute_url(self):
        return reverse('directories:genre_list')

class Editor(models.Model):
    editor = models.CharField(
        verbose_name='Издательство',
        max_length=30)

    class Meta:
        verbose_name = "Издательство",
        verbose_name_plural = "Издательства" 

    def __str__(self) -> str:
        return self.editor

    def get_absolute_url(self):
        return reverse('directories:editor_list')