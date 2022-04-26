from django.urls import path, include
from . import views as order_views

app_name = 'orders'

urlpatterns = [
    path('create_order', order_views.CreateOrderView.as_view(), name='create_order'),  
    path('list_order', order_views.ListOrderView.as_view(), name='list_order'),     
    path('detail_order/<int:pk>/', order_views.OrderDetailView.as_view(), name='detail_order'),
    #path('order_stat_update/<int:pk>/', order_views.OrderStatusUpdateView.as_view(), name='order_stat_update'),   
    path('order_stat_update/', order_views.OrderStatusUpdateView.as_view(), name='order_stat_update'),  
]