from django.urls import path, include
from . import views 

app_name = 'comments'

urlpatterns = [
    path('create_comment>', views.CommentCreateView.as_view(), name='create_comment'),  
]