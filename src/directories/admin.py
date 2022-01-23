from django.contrib import admin

# Register your models here.

from . import models

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author']

class SerieAdmin(admin.ModelAdmin):
    list_display = ['pk', 'serie']

class GenreAdmin(admin.ModelAdmin):
    list_display = ['pk', 'genre']

class EditorAdmin(admin.ModelAdmin):
    list_display = ['pk', 'editor']

admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Serie, SerieAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Editor, EditorAdmin)