from cProfile import label
from dataclasses import fields
from pyexpat import model
from django import forms

from . import models

class AuthorCreateForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = {
            'author',
        }


class SerieCreateForm(forms.ModelForm):
    class Meta:
        model = models.Serie
        fields = {
            'serie',
        }


class GenreCreateForm(forms.ModelForm):
    class Meta:
        model = models.Genre
        fields = {
            'genre',
        }

class EditorCreateForm(forms.ModelForm):
    class Meta:
        model = models.Editor
        fields = {
            'editor',
        }


#OLD FASSHION METHOD:
#class AuthorCreateForm(forms.Form):
#    author = forms.CharField(
#        max_length=100,
#        min_length=1,
#        required=True,
#        label = "Author",
#    )