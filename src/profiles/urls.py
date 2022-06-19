from django.urls import path
from . import views as profile_views

app_name = 'profiles'

urlpatterns = [ 
    path('register/', profile_views.RegisterFormView.as_view(), name='register'),  
    path('login/', profile_views.UserLoginView.as_view(), name='login'), 
    path('logout/', profile_views.UserLogoutView.as_view(), name='logout'), 
    path('profile_user/', profile_views.UpdateRegisterView.as_view(), name='profile_user'),
    path('password_change_form/', profile_views.UserPasswordChangeView.as_view(), name='password_change'),  
    path('profile_data/<int:pk>/', profile_views.UserDataDetaiView.as_view(), name='profile_data'),
    path('skip_pass/', profile_views.UserPassordMailView.as_view(), name='skip_pass'),
]

