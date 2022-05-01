from django.contrib import admin
from . import models

class OrderStatusAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'order_status',
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'cart',
        'contact_info',
        'created',
        'updated',
        'order_status',
    ]  



admin.site.register(models.OrderStatus, OrderStatusAdmin)
admin.site.register(models.Order, OrderAdmin)
