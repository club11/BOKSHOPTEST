from django.contrib import admin
from . import models

class OrderStatusAdmin(admin.ModelAdmin):
    list_display = [
        'order_status',
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'cart',
        'order_status',
        'contact_info',
        'created',
        'updated',
    ]  



admin.site.register(models.OrderStatus, OrderStatusAdmin)
admin.site.register(models.Order, OrderAdmin)
