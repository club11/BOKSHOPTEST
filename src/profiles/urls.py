from django.urls import path
from . import views as profile_views

app_name = 'profiles'

urlpatterns = [ 
    path('register/', profile_views.RegisterFormView.as_view(), name='register'),  

    path('logout/', profile_views.UserLogoutView.as_view(), name='logout'), 

]