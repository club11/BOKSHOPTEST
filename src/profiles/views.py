from pyexpat import model
from django.views.generic import FormView
from . import forms
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

from profiles.models import User, Profile

class RegisterFormView(FormView):
    template_name = 'profiles/register_user.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('books:home')

    def form_valid(self, form):                         #создаем юзера и профиль в БД
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')
        tel = form.cleaned_data.get('tel')
        user = User.objects.create_user(username=username,password=password)
        profile = Profile.objects.create(user=user, tel=tel)
        login(self.request, user)                       #логиним юзера
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    template_name = 'books/book_list.html'