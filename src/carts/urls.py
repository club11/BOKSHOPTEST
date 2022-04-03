from django.urls import path, include
from . import views as cart_views

app_name = 'carts'

urlpatterns = [
    #path('cart_detail/<int:pk>/', cart_views.CartView.as_view(), name='cart'),   
    path('', cart_views.CartView.as_view(), name='cart'),  
    path('delete_good_in_cart/<int:pk>', cart_views.GoodInCartDeleteView.as_view(), name='delete_good_in_cart'),  
    path('update_cart/', cart_views.CartUpdate.as_view(), name='update_cart'), 
]