from django.urls import path, include
from . import views as order_views

app_name = 'orders'

urlpatterns = [
    path('create_order', order_views.CreateOrderView.as_view(), name='create_order'),  
]