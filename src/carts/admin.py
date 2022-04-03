from pyexpat import model
from symtable import Class
from django.contrib import admin

from . import models

class CartAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
    ]

class BookInCartAdmin(admin.ModelAdmin):
    list_display = [
        'book',
        'quantity',
        'unit_price',
        'cart',
    ]

admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.BookInCart, BookInCartAdmin)
