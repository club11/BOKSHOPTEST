from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views as books_views

app_name = 'books'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  books_views.HomeTemplateView.as_view(), name='home'),  
    path('book_list/',  books_views.BookListView.as_view(), name='book_list'),   
    path('book-_goods_list/',  books_views.BookasGoodsListView.as_view(), name='book_goods_list'), 
    path('book_detail/<int:pk>/', books_views.BookDetailView.as_view(), name='book'),   
    path('book_create/', books_views.BookCreateView.as_view(), name='book_create'),  
    path('book_update/<int:pk>/', books_views.BookUpdateView.as_view(), name='book_update'), 
    path('book_delete/<int:pk>/', books_views.BookDeleteView.as_view(), name='book_delete'), 
#    path('add-rating/', books_views.AddStarRaing.as_view(), name='add_rating'), 
]