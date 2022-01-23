from tabnanny import verbose
from django.db import models

# Create your models here.


class Author(models.Model):
    author = models.CharField(
        verbose_name='Автор',
        max_length=30)

    class Meta:
        verbose_name = "Автор",
        verbose_name_plural = "Авторы" 

class Serie(models.Model):
    serie = models.CharField(
        verbose_name='Серия',
        max_length=30)

    class Meta:
        verbose_name = "Серия",
        verbose_name_plural = "Серии" 


class Genre(models.Model):
    genre = models.CharField(
        verbose_name='Жанр',
        max_length=30)

    class Meta:
        verbose_name = "Жанр",
        verbose_name_plural = "Жанры" 


class Editor(models.Model):
    editor = models.CharField(
        verbose_name='Издательство',
        max_length=30)

    class Meta:
        verbose_name = "Издательство",
        verbose_name_plural = "Издательства" 