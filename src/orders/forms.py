from dataclasses import field, fields
from email.policy import default
from turtle import color
from django import forms

from orders import models
from validators.validators import tel_validator

class OrderCreateForm(forms.Form):            #стартуем с обычной формы не привязанной
    contact_info = forms.CharField(label='контактные данные', widget=forms.TimeInput, disabled=True, required=None,) # вах! изучить
    tel = forms.CharField(label='номер телефона', required=True, max_length=20, help_text='+37529XXXXXXX', validators=[tel_validator])






