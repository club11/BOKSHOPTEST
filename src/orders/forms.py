from dataclasses import field, fields
from email.policy import default
from django import forms

class OrderCreateForm(forms.Form):            #стартуем с обычной формы не привязанной
    contact_info = forms.CharField(label='контактные данные', required=True, widget=forms.TimeInput) # вах! изучить
    tel = forms.CharField(label='номер телефона', required=False, max_length=20)
