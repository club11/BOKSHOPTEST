
#from asyncio.windows_events import NULL

from audioop import reverse
from contextlib import nullcontext
import email
from posixpath import split
from pyexpat import model
from django.shortcuts import render
from requests import request
import books
from books import models
from profiles import models as profile_models
import carts
from carts.models import Cart, User
from . import models, forms
from . models import Order, carts_models, profiles_models
from django.views.generic import FormView, ListView, DetailView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q 
from django.contrib.auth.mixins import PermissionRequiredMixin

class CreateOrderView(FormView):
    form_class = forms.OrderCreateForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('books:home')

    def get_initial(self):                      # подкидывем доп данные в заказ(телефон и прочее из данных ппользователя)
        if self.request.user.is_anonymous:
            return {'contact_info': '', 'tel':' '}
        username = self.request.user.get_username()
        tel = self.request.user.profile.tel
        return {'contact_info': username, 'tel':tel}

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')               #обращаемся к СЕССИИ текущей за корзины id
        cart, created = carts_models.Cart.objects.get_or_create(          #распаковка тапла
            pk=cart_id,                                       # поле по которому производится поиск
            defaults={},
        )
        #if cart.cart_total_price() is NULL:  
        if cart.cart_total_price() == 0 or cart.cart_total_price() < 0:                                                                                            #ЕСЛИ ЗАКАЗ ПУСТОЙ
            messages.add_message(self.request, messages.INFO, 'Ваша корзина пуста')            # отправляем сообщение пользователю
            return HttpResponseRedirect(reverse_lazy('orders:create_order'))                                                            #ЕСЛИ ЗАКАЗ ПУСТОЙ  
        if created:
            return HttpResponseRedirect(reverse_lazy('carts:cart'))
        ci = form.cleaned_data.get('contact_info')                             # Неочевидный ход через форму
        orderstatus = models.OrderStatus.objects.get(pk=1)
        if self.request.user.is_anonymous:
            order = models.Order.objects.create(
                cart=cart,
                contact_info = ci,
                tel = form.cleaned_data.get('tel'),
                order_status = orderstatus
            ) 
        else:
            user= self.request.user                                 #подкидываем почту в модель заказа если не анонимус
            email = profiles_models.Profile.objects.get(user=user).email #подкидываем почту в модель заказа если не анонимус
            order = models.Order.objects.create(
                cart=cart,
                contact_info=ci,
                order_status = orderstatus,
                tel= form.cleaned_data.get('tel'),
                email_adress = email                           #подкидываем почту в модель заказа если не анонимус
            ) 
        del self.request.session['cart_id']         #чистим сессию bad luck
        #self.request.session.delete('cart_id')    #чистим сессию bad luck / riginal method ain't workin'
        books_in_cart = order.cart.cart.all()               ##### # отправляем сообщение пользователю (подготовка перечня названий книг)
        book_names = []
        for n in range(0, books_in_cart.count()):
            names = books_in_cart[n].book.book_name
            book_names.append(names)    
        book_names_str = ''.join(book_names)
        if self.request.user.is_authenticated:
            user = self.request.user                                                #
            user_email_profile = profiles_models.Profile.objects.get(user=user)     # получаем адрес почты для уведомления
            user_email = user_email_profile.email                                   #
            if user_email:
                messages.add_message(self.request, messages.INFO, f'{str(self.request.user)} , Ваш заказ {book_names_str} принят в обработку. Уведомление о подтверждении будет направлено на Ваш почтовый адресс {user_email}')            # отправляем сообщение пользователю
            else:
                messages.add_message(self.request, messages.INFO, f'{str(self.request.user)} , Ваш заказ {book_names_str} принят в обработку.')
        else:
            tel = form.cleaned_data.get('tel')
            messages.add_message(self.request, messages.INFO, f'{str(self.request.user)} , Ваш заказ {book_names_str} принят в обработку. Для уточнения заказа с Вами свяжется наш менеджер по указанному телефону {tel}')
        #return HttpResponseRedirect(reverse_lazy('books:book_goods_list'))

        #####################################
        ## убираем количество доступных для заказа книг в случае создания заказа
        delete_book_quantity_list =[]                       # получаем список количество книг для уменьшения
        book_in_cart_list =[]
        for i in books_in_cart:
            delete_book_quantity_list.append(i.quantity)
            book_in_cart_list.append(i.book)
        for b in book_in_cart_list:
            n = 0
            b.value_available -= delete_book_quantity_list[n]
            n += 1
            b.is_available_validator()
            b.save()
        #####################################

        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('books:book_goods_list'))
        else:
            return HttpResponseRedirect(reverse_lazy('orders:my_list_order'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')               #обращаемся к СЕССИИ текущей за корзины id
        cart, created = carts_models.Cart.objects.get_or_create(          #распаковка тапла
            pk=cart_id,                                       # поле по которому производится поиск
            defaults={},
        )       
        context['object'] = cart
        return context 
class ListOrderView(PermissionRequiredMixin,LoginRequiredMixin, ListView):
    model = models.Order
    template_name = 'orders/list_order.html'
    paginate_by = 30
    login_url = reverse_lazy('profiles:login')
    permission_required = 'orders.view_order'

    def get_queryset(self):                                 # поиск по заказчику
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(contact_info__icontains=q))     
        return queryset  
            
    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        context['search_request'] = q
        return context 

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        order_contact_info = self.request.GET.get('profile')
        if order_contact_info is None:
            pass
        elif order_contact_info:
            get_user = User.objects.get(username=order_contact_info)
            get_user_profile = profiles_models.Profile.objects.get(user=get_user)
            return HttpResponseRedirect(reverse_lazy('profiles:profile_data', args=[get_user_profile.pk]))
        return response

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = models.Order
    template_name = 'orders/detail_order.html'
    #success_url = reverse_lazy('orders:list_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_stat_current = self.get_object().order_status.pk
        if order_stat_current == 4:
            context['denied'] = order_stat_current
        return context

class OrderStatusUpdateView(View):

    def post(self, request, **kwargs):
        order_status_pk = self.request.POST.get('order_status')
        obj_pk = self.request.POST.get('order')
        obj = models.Order.objects.get(pk=obj_pk)
        order_status_values_list = models.OrderStatus.objects.values_list()
        order_status_num = order_status_values_list.count()                                   #проверка на наличие зарегестрированного пользователя путем наличия имени пользователя в заказ
        if order_status_pk.isalpha() is True:
            return HttpResponseRedirect(reverse_lazy('orders:detail_order', args = [obj_pk]))
        else:            
            order_status_current_pk_position = int(order_status_pk)
            if order_status_current_pk_position in range(order_status_num + 1):
                new_order_status = models.OrderStatus.objects.get(pk=int(order_status_pk))      
                obj.order_status = new_order_status
                obj.save()

                #email = models.Order.objects.get(pk=obj_pk).email_adress        #получаем почту от зарегенного пользователя
                email = ''
                if obj.contact_info != '':
                    user_order_name = obj.contact_info
                    user_order = User.objects.get(username=user_order_name)
                    user_email_profile = profiles_models.Profile.objects.get(user=user_order)  
                    email = user_email_profile.email

                    if new_order_status.order_status == 'принят': # если статус заказа изменяется на ПРИНЯТ и есть почтовый адрес то отправить сообщение в почту
                    #if new_order_status.order_status == 'принят' and email is not None: # если статус заказа изменяется на ПРИНЯТ и есть почтовый адрес то отправить сообщение в почту
                        order = models.Order.objects.get(pk=obj_pk)
                        books_in_cart = order.cart.cart.all()               ##### # отправляем сообщение пользователю на почту (подготовка перечня названий книг)
                        book_names = ['Ваш заказ принят:']
                        for n in range(0, books_in_cart.count()):
                            names = books_in_cart[n].book.book_name
                            book_names.append(names)    
                        book_names_str = ''.join(book_names)
                        order_adress = self.request.get_full_path_info()
                        send_mail(      
                            book_names_str,                     # строка от сабжэкт
                            order_adress,                       # строка суть письма - в данном случае адресс на заказ (ДОРАБОТАТЬ ФУЛЛ путь)
                            'club11bookshop@mail.ru',           # отправитель
                            [user_email_profile.email],                       # получатель
                            fail_silently=True,             #в FALSE указывает об ошибке неотправленного письма для девеломпента / в боевом серваке статус TRue
                        )
                        messages.add_message(self.request, messages.SUCCESS, f'Уведомление об изменении статуса заказа на "принят" направлено на почтовый адресс {user_email_profile.email}')
                if new_order_status.order_status == 'отменен':
                    print('PIzdec')
                    #####################################
                    ## убираем количество доступных для заказа книг в случае создания заказа
                    delete_book_quantity_list =[]                       # получаем список количество книг для уменьшения
                    book_in_cart_list =[]
                    order = models.Order.objects.get(pk=obj_pk)
                    books_in_cart = order.cart.cart.all() 
                    for i in books_in_cart:
                        book_in_cart_list.append(i.book)
                    print(book_in_cart_list)
                    for i in books_in_cart:
                        delete_book_quantity_list.append(i.quantity)
                    print(delete_book_quantity_list)                    
                    for b in book_in_cart_list:
                        n = 0
                        b.value_available += delete_book_quantity_list[n]
                        n += 1
                        b.is_available_validator()
                        b.save()
                    #####################################
        user = self.request.user
        users_groups = user.groups.filter(name__contains='staff')  
        if users_groups:
            return HttpResponseRedirect(reverse_lazy('orders:list_order'))
        else:
            return HttpResponseRedirect(reverse_lazy('orders:my_list_order'))
   
class MyListOrderView(LoginRequiredMixin, ListView):
    model = models.Order
    template_name = 'orders/my_list_order.html'
    paginate_by = 30
    login_url = reverse_lazy('profiles:login')

    def get_queryset(self):
        username = self.request.user.get_username()
        order = models.Order.objects.filter(contact_info=username)
        #queryset = super().get_queryset()
        queryset = order
        return queryset

