from asyncio.windows_events import NULL
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password

from profiles.models import User

username_validator = UnicodeUsernameValidator()    #создаем один из валидаторов из библиотеки    


def tel_validator(value):               # самодельный валидатор номера телефона
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if value[0] != '+':
        raise ValidationError('код должен начинаться с "+" ')
    for i in value[1:]:
        if i not in numbers:
            raise ValidationError('введены некорректные данные номера телефона ')
    return value

def user_name_unique(value):        # самодельный валидатор уникальности имени пользователя
    #user_name = str(User.objects.filter(username__icontains=value))                  # кстати, вот прикольна фильтруха     user_name = User.objects.values_list('username')
    user_name = User.objects.filter(username__icontains=value)
    if user_name.count() > 0 and value == str(user_name[0]):
        raise ValidationError('пользователь с данным именем уже зарегестрирован')
    return value

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