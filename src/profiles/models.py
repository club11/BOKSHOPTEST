from tabnanny import verbose
from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()             #активная в настоящий момент юзерская модель

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='Имя аккаунта',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    tel = models.CharField(verbose_name='номер телефона', max_length=20)
    
