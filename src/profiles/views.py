from pyexpat import model
from django.views.generic import FormView
from requests import request
from . import forms
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView


from profiles.models import User, Profile

class UserLoginView(LoginView):
    template_name = 'profiles/login.html'
    #next = reverse_lazy('books:home')

    def get_redirect_url(self):
            next = reverse_lazy('books:home')
            return next
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
    template_name = 'books/home.html'

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

# ИЗМЕНЕНИЕ ПАРОЛЯ ВЕР 
#################
    #def password_change(request):
    #    if request.method == 'POST':
    #        form = forms.UpdateRegisterForm(user=request.user, data=request.POST)
    #        if form.is_valid():
    #            form.save()
    #            update_session_auth_hash(request, form.user)

# ИЗМЕНЕНИЕ ПАРОЛЯ
###############################################################
    #        user = User.objects.get(username=username)
    #    user.set_password(password)           # изменить пароль
    #    user.save()
##########################################################

# ПЕРЕАДРЕСАЦИЯ ПОСЛЕ ЗАЛОГИНИВАНИЯ
###########################################################
    ###def get_redirect_url(self):
    ###    if self.request.GET:
    ###        previous_page = self.request.get_full_path().split('?/')
    ###        print( previous_page) 
    ###        previous_page = self.request.get_full_path().split('?/')[1]     
    ###        next_page_list = str(previous_page.split('/')) 
    ###        print(type(next_page_list))
    ###        print(next_page_list)
    ###        next_page_list = str(next_page_list)
    ###        print(next_page_list)
    ###        next_page_list = next_page_list.rstrip('')
    ###        print('NNNNNN', next_page_list)
    ###        print(type(next_page_list))
    ###    next = next_page_list
    ###    if self.request.POST:
    ###        next = reverse_lazy('books:home')
    ###    return next
    ###    #next = reverse_lazy('books:home')

    #def current_page(self):
    ########################################################