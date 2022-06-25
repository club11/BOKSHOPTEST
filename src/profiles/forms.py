
from cProfile import label
from dataclasses import fields
import email
from enum import unique
from wsgiref.validate import validator
from django import forms
from django.contrib.auth import password_validation
from requests import request
from . import models

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

from validators.validators import tel_validator, user_name_unique, ValidationError
from django.core.validators import validate_email

from profiles.models import User

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

username_validator = UnicodeUsernameValidator()    #создаем один из валидаторов из библиотеки    
from django.contrib.auth import get_user_model
class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=50,
        required=True,
        label='Имя пользователя',
        validators=[username_validator],
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Пароли не совпадают. Повторите пароль для проведения валидации.",
    )   

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        label='Имя пользователя',
        validators=[username_validator, user_name_unique],
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Пароли не совпадают. Повторите пароль для проведения валидации.",
    )
    tel = forms.CharField(
        max_length=20,
        required=True,
        label='Номер телефона',
        help_text='+37529XXXXXXX',
        validators=[tel_validator]
    )

    def clean_password2(self):                              #еще валидатор
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                "пароли не совпадают",
                code="password_mismatch",
            )
        try:
            validate_password(password2, User)
        except ValidationError as error:
            self.add_error('password2', error)
        return password2

#class UpdateRegisterForm(RegisterForm):
#    class Meta:
#        fields

def user_updatename_unique(value):        # самодельный валидатор уникальности имени ЗАРЕГЕСТРИРОВАННОГО пользователя
    #user_name = str(User.objects.filter(username__icontains=value))                  # кстати, вот прикольна фильтруха     user_name = User.objects.values_list('username')
    user_name = User.objects.filter(username__icontains=value)
    #print(value, 'XXX', str(user_name[0]), 'XXX',)
    if value == str(user_name[0]):
        return value        
    else:
        if user_name.count() > 0 and value == str(user_name[0]):
            raise ValidationError('пользователь с данным именем уже зарегестрирован')
    return value
class  UserPassordMailForm(forms.Form):
    email = forms.EmailField(
        label = 'email',
        widget = forms.EmailInput(),
        validators = [validate_email]
    )   

class UpdateRegisterForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        label='Имя пользователя',
        validators=[username_validator],
    )
    tel = forms.CharField(
        max_length=20,
        required=True,
        label='Номер телефона',
        help_text='+37529XXXXXXX',
        validators=[tel_validator]
    )
    email = forms.EmailField(
        label = 'email',
        widget=forms.EmailInput()
    )
    first_name = forms.CharField(max_length=20, label='Имя', required=False)
    last_name = forms.CharField(max_length=20, label='Фамилия', required=False)
    country = forms.CharField(max_length=20, label='Страна', required=False) 
    index  = forms.IntegerField(label='Индекс', required=False)
    adress = forms.CharField(max_length=30, label='Адресс', required=False)

    def clean_email(self):
        #value = self.cleaned_data.get('email')
        new_data__email = self.cleaned_data['email']
        initial_data__email = self.initial.get('email')       # первоначальные данные в поле таблицы
        profile_exist = models.Profile.objects.filter(email=new_data__email)
        if profile_exist:
            get_profile_exist = models.Profile.objects.get(email=new_data__email)     
            if new_data__email == get_profile_exist.email:
                if new_data__email == initial_data__email:
                    print('не думаю!')                      #юзерм введен его же тот же самый почтовый адрес повторно
                    pass
                else:
                    print('Совпадение!',)
                    raise ValidationError('данный почтовый адрес зарегестрирован на другого пользователя')
        return new_data__email
