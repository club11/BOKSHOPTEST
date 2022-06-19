from dataclasses import fields
from email.headerregistry import Group
from itertools import count
from pipes import Template
from pyexpat import model
from unicodedata import name
from django.views.generic import FormView
from requests import request
from profiles import models
from . import forms
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.views.generic import DetailView
from profiles.models import User, Profile
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
import string
import random
from django.contrib import messages
class UserLoginView(LoginView):
    template_name = 'profiles/login.html'
    next_page = next

    def get_success_url(self):                                                  # перенаправить юзера staff на иную страницу
        user = self.request.user
        users_groups = user.groups.filter(name__contains='staff')
        if users_groups.count() > 0:
            staff_group = user.groups.get(name = 'staff')
            if staff_group.name == 'staff':
                return reverse_lazy('books:book_list')                  # ПЕРЕНАПРАВИТ здесь
        #return super().get_success_url()
        return reverse_lazy('profiles:profile_user')


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
        current_user = self.request.user
        get_profile = Profile.objects.get(user=current_user)
        get_profile.tel=tel
        get_profile.email=email
        get_profile.first_name=first_name 
        get_profile.last_name=last_name 
        get_profile.country=country
        get_profile.city=city
        get_profile.index=index 
        get_profile.adress=adress
        get_profile.save()
        #profile = Profile.objects.update(tel=tel, email=email, first_name=first_name, last_name=last_name, country=country, city=city, index=index, adress=adress)
        return super().form_valid(form)

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'profiles/password_change_form.html'
    success_url = reverse_lazy('profiles:profile_user')

class UserDataDetaiView(DetailView):
    model = models.Profile
    template_name = 'profiles/profile_data.html'

class UserPassordMailView(FormView):
    template_name = 'profiles/skip_pass.html'
    form_class = forms.UserPassordMailForm
    success_url = reverse_lazy('profiles:login')

    def form_valid(self, form):
        email_adress = form.cleaned_data.get('email')
        profile = models.Profile.objects.get(email=email_adress)
        user = User.objects.get(username=profile.user)
        ################# generate random password
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        length = 8
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        #################
        #print("".join(password))
        user.set_password("".join(password))
        user.save()
        #print(user.password)
        send_mail(      
            'поступил запрос на изменения пароля',                     # строка от сабжэкт
            f'Ваш пароль к аккаунту {user.username} в изменен на {"".join(password)}',                       # строка суть письма - в данном случае адресс на заказ (ДОРАБОТАТЬ ФУЛЛ путь)
            'club11bookshop@mail.ru',           # отправитель
            [email_adress],                       # получатель
            fail_silently=True,             #в FALSE указывает об ошибке неотправленного письма для девеломпента / в боевом серваке статус TRue
        )
        messages.add_message(self.request, messages.INFO, f'Уведомление о смене пароля направлено на Ваш почтовый адресс {email_adress}')
        return super().form_valid(form)
