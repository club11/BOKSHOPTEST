import email
from tabnanny import verbose
from tkinter import CASCADE
from unittest import mock
from django.db import models
from carts import models as carts_models
from profiles import models as profiles_models

class OrderStatus(models.Model):
    order_status = models.CharField(
        verbose_name='статус заказа',
        max_length=20,
        blank=True,
        null=True,
        default='новый',
    )

class Order(models.Model):
    cart = models.ForeignKey(
        carts_models.Cart,
        on_delete=models.PROTECT,
        verbose_name='заказ',
    )
    order_status = models.ForeignKey(
        OrderStatus,
        verbose_name='статус заказа',
        related_name='orderstatus',
        on_delete=models.PROTECT 
    )
    #contact_info =  User or
    contact_info = models.TextField(
        verbose_name='контактная информация',
        blank=True,
        null=False
    )
    created = models.DateTimeField(
        verbose_name='создан',
        auto_now=False,
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name='обновлен',
        auto_now=True,
        auto_now_add=False
    )
    tel = models.CharField(
        verbose_name='телефон',
        max_length = 20,
        default='+375XX XXX XX XX'
    )
    email_adress = models.EmailField(
        verbose_name='email', 
        null=True
    )

