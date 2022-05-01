from django.core.exceptions import ValidationError
from profiles.models import User

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