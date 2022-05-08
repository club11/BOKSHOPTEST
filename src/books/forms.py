from dataclasses import fields
from xml.parsers.expat import model
from . import models
from django import forms
from django.urls import reverse

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = {
            'book_name',
            'picture',
            'price',
            'currency_price',
            'author',
            'serie',
            'genre',
            'editor',
            'publishing_date',
            'pages',
            'binding',
            'format',
            'isbn',
            'weigh',
            'age_restrictions',
            'value_available',
            'available',
            #'rating',
        }


########################################################
#доработать рейтинг
class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=models.RatingStar.objects.all(),       # сбор знчений квэрисэтом!
        widget=forms.RadioSelect,
        empty_label=None
    )

    class Meta:
        model = models.Rating
        fields = ('star',)          # переопределить поле на ModelChoiceField формы (удобно!)
######################################################       
        