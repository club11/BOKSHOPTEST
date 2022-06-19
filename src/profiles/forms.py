from asyncio.windows_events import NULL
from cProfile import label
from dataclasses import fields
import email
from wsgiref.validate import validator
from django import forms
from django.contrib.auth import password_validation
from . import models

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

from validators.validators import tel_validator, user_name_unique, ValidationError

from profiles.models import User

username_validator = UnicodeUsernameValidator()    #создаем один из валидаторов из библиотеки    

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

def email_adress_unique(value):
    email_exist = models.Profile.objects.filter(email__iexact=value)
    if email_exist:
        raise ValidationError('пользователь с данным почтовым адресом уже зарегестрирован')
    else:
        return value 

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
        widget=forms.EmailInput(),
        validators=[email_adress_unique,]
    )
    first_name = forms.CharField(max_length=20, label='Имя',)
    last_name = forms.CharField(max_length=20, label='Фамилия',)
    country = forms.CharField(max_length=20, label='Страна',)
    index  = forms.IntegerField(label='Индекс')
    adress = forms.CharField(max_length=20, label='Адресс',)

    #def clean_password2(self):                              #еще валидатор
    #    password1 = self.cleaned_data.get("password1")
    #    password2 = self.cleaned_data.get("password2")
    #    if password1 and password2 and password1 != password2:
    #        raise ValidationError(
    #            "пароли не совпадают",
    #            code="password_mismatch",
    #        )
    #    try:
    #        validate_password(password2, User)
    #    except ValidationError as error:
    #        self.add_error('password2', error)
    #    return password2

#class UserPassordMailForm(forms.ModelForm):
#    class Meta:
#        model = models.Profile
#        fields = ('email',)
#        validator = [email_valid]

def email_valid(value):        # самодельный валидатор уникальности имени ЗАРЕГЕСТРИРОВАННОГО пользователя
    #user_name = models.Profile.objects.filter(email__iexact=value)
    user_name = models.Profile.objects.get(email=value)
    if user_name:
        return value        
    else:
        raise ValidationError('Пользователя с таким e-mail не существует')
    return value

class  UserPassordMailForm(forms.Form):
     email = forms.EmailField(
        label = 'email',
        widget=forms.EmailInput(),
        validators = [email_valid]
    )   