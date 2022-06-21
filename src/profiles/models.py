from tabnanny import verbose
from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.contrib.auth import update_session_auth_hash

User = get_user_model()             #активная в настоящий момент юзерская модель

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='Имя аккаунта',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    tel = models.CharField(verbose_name='номер телефона', max_length=20, null=True)
    email = models.EmailField(verbose_name='email', null=True)
    first_name = models.CharField(verbose_name='имя', max_length=20, null=True)
    last_name = models.CharField(verbose_name='фамилия', max_length=20, null=True)
    #group
    country = models.CharField(verbose_name='страна', max_length=20, null=True)
    city = models.CharField(verbose_name='город', max_length=20, null=True)
    index = models.IntegerField(verbose_name='индекс', null=True)
    adress = models.CharField(verbose_name='адрес', max_length=30, null=True)