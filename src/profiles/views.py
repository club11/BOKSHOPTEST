from email.headerregistry import Group
from itertools import count
from pyexpat import model
from unicodedata import name
from django.views.generic import FormView
from requests import request
from profiles import models
from . import forms
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from profiles.models import User, Profile
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse

class UserLoginView(LoginView):
    template_name = 'profiles/login.html'
    next_page = reverse_lazy('profiles:profile_user')

    def get_success_url(self):                                                  # перенаправить юзера staff на иную страницу
        user = self.request.user
        users_groups = user.groups.filter(name__contains='staff')
        if users_groups.count() > 0:
            staff_group = user.groups.get(name = 'staff')
            if staff_group.name == 'staff':
                return reverse_lazy('books:book_list')                  # ПЕРЕНАПРАВИТ здесь
        return super().get_success_url()

class RegisterFormView(FormView):
    template_name = 'profiles/register_user.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('books:home')

    permission = Permission.objects.filter(name__in =['Can add comment', 
        'Can change comment',
        'Can view comment', 
        'Can add order', 
        'Can view order', 
        'Can change order status',
        'Can view order status',
        'Can add profile',
        'Can change profile',
        'Can view profile',
        'Can view author']
        )
    customer_group = Group.objects.get(name='test_group')                #добавить зарегестрированного пользователя в ГРУППУ кастомеры
    customer_group.permissions.set(permission)

    def form_valid(self, form):                         #создаем юзера и профиль в БД
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')
        tel = form.cleaned_data.get('tel')
        user = User.objects.create_user(username=username,password=password)
        profile = Profile.objects.create(user=user, tel=tel)
        login(self.request, user)                       #логиним юзера

        user.groups.add(self.customer_group)                                     #добавить зарегестрированного пользователя в ГРУППУ кастомеры
        #user.user_permissions.set(self.permission)                              #ТЕРМИТЫ
        #print(user.groups.all(), user.user_permissions.all(), 'IIIIIIIIIII', user.get_group_permissions(), 'IIIII')          
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    template_name = 'books/home.html'
    next_page = reverse_lazy('books:home')

class UpdateRegisterView(FormView):
    template_name = 'profiles/profile_user.html'
    form_class = forms.UpdateRegisterForm
    success_url = reverse_lazy('profiles:profile_user')

    def get_initial(self):
        if self.request.user.is_anonymous:
            return {}
        username = self.request.user.get_username()
        #password = self.request.user.set_password
        tel = self.request.user.profile.tel
        email = self.request.user.profile.email
        first_name = self.request.user.profile.first_name
        last_name = self.request.user.profile.last_name
        country  = self.request.user.profile.country
        city = self.request.user.profile.city
        index = self.request.user.profile.index
        adress = self.request.user.profile.adress
        return {'username': username, 'tel':tel, 'email':email, 'first_name':first_name, 'last_name':last_name, 'country':country, 'city':city, 'index':index, 'adress':adress, }

    def form_valid(self, form):                         #создаем юзера и профиль в БД
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')
        tel = form.cleaned_data.get('tel')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        country = form.cleaned_data.get('country')
        city = form.cleaned_data.get('city')
        index = form.cleaned_data.get('index')
        adress = form.cleaned_data.get('adress')        #profile = Profile.objects.update(user=user, tel=tel, email=email, first_name=first_name, last_name=last_name, country=country, city=city, index=index, adress=adress)
        ##############
        username_old = self.request.user.get_username()        
        user = User.objects.get(username=username_old)
        user.username = username
        user.save()
        ###############
        profile = Profile.objects.update(tel=tel, email=email, first_name=first_name, last_name=last_name, country=country, city=city, index=index, adress=adress)
        return super().form_valid(form)

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'profiles/password_change_form.html'
    success_url = reverse_lazy('profiles:profile_user')

