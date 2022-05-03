from asyncio.windows_events import NULL
from audioop import reverse
from contextlib import nullcontext
from posixpath import split
from pyexpat import model
from django.shortcuts import render
from requests import request
import books
from books import models
from carts.models import Cart, User
from . import models, forms
from . models import Order, carts_models, profiles_models
from django.views.generic import FormView, ListView, DetailView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail

class CreateOrderView(FormView):
    form_class = forms.OrderCreateForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('books:home')

    def get_initial(self):                      # подкидывем доп данные в заказ(телефон и прочее из данных ппользователя)
        if self.request.user.is_anonymous:
            return {'contact_info': ' ', 'tel':' '}
        username = self.request.user.get_username()
        tel = self.request.user.profile.tel
        return {'contact_info': username, 'tel':tel}

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')               #обращаемся к СЕССИИ текущей за корзины id
        cart, created = carts_models.Cart.objects.get_or_create(          #распаковка тапла
            pk=cart_id,                                       # поле по которому производится поиск
            defaults={},
        )
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
            order = models.Order.objects.create(
                cart=cart,
                contact_info=ci,
                order_status = orderstatus,
                tel= form.cleaned_data.get('tel'),
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
            messages.add_message(self.request, messages.INFO, f'{str(self.request.user)} , Ваш заказ {book_names_str} принят в обработку. Уведомление о подтверждении будет направлено на Ваш почтовый адресс {user_email}')            # отправляем сообщение пользователю
        else:
            tel = form.cleaned_data.get('tel')
            messages.add_message(self.request, messages.INFO, f'{str(self.request.user)} , Ваш заказ {book_names_str} принят в обработку. Для уточнения заказа с Вами свяжется наш менеджер по указанному телефону {tel}')
        #return HttpResponseRedirect(reverse_lazy('books:book_goods_list'))
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('orders:list_order'))
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
class ListOrderView(ListView):
    model = models.Order
    template_name = 'orders/list_order.html'
    paginate_by = 30

class OrderDetailView(DetailView):
    model = models.Order
    template_name = 'orders/detail_order.html'
    success_url = reverse_lazy('orders:list_order')

class OrderStatusUpdateView(View):

    #def get_email(self):
    #    order_pk = self.request.POST.get('order_status')
    #    print(order_pk)
    #    tel = models.Order.objects.get(pk=order_pk).tel
    #    email_exist = profiles_models.Profile.objects.filter(tel=tel)
    #    print(email_exist)

    #def post(self, request, pk):
    def post(self, request, **kwargs):
        order_status_pk = self.request.POST.get('order_status')
        obj_pk = self.request.POST.get('order')
        obj = models.Order.objects.get(pk=obj_pk)
        order_status_values_list = models.OrderStatus.objects.values_list()
        order_status_num = order_status_values_list.count()
                                                                        #проверка на наличие зарегестрированного пользователя путем наличия имени пользователя в заказе

        obj_pk = self.request.POST.get('order')
        tel = models.Order.objects.get(pk=obj_pk).cart.customer
        print(tel)
        #email_exist = profiles_models.Profile.objects.filter(tel=tel)
        #print(email_exist)



        if order_status_pk.isalpha() is True:
            return HttpResponseRedirect(reverse_lazy('orders:list_order'))
        else:            
            order_status_current_pk_position = int(order_status_pk)
            if order_status_current_pk_position in range(order_status_num + 1):
                new_order_status = models.OrderStatus.objects.get(pk=int(order_status_pk))      
                obj.order_status = new_order_status
                obj.save()
                if new_order_status.order_status == 'принят':
                    order = models.Order.objects.get(pk=obj_pk)
                    books_in_cart = order.cart.cart.all()               ##### # отправляем сообщение пользователю на почту (подготовка перечня названий книг)
                    book_names = ['Ваш заказ принят:']
                    for n in range(0, books_in_cart.count()):
                        names = books_in_cart[n].book.book_name
                        book_names.append(names)    
                    book_names_str = ''.join(book_names)
                    order_adress = self.request.get_full_path_info()
                    user = self.request.user
                    user_email_profile = profiles_models.Profile.objects.get(user=user)
                    user_email = user_email_profile.email
                    send_mail(      
                        book_names_str,                     # строка от сабжэкт
                        order_adress,                       # строка суть письма - в данном случае адресс на заказ (ДОРАБОТАТЬ ФУЛЛ путь)
                        'club11bookshop@mail.ru',           # отправитель
                        [user_email],                       # получатель
                        fail_silently=True,             #в FALSE указывает об ошибке неотправленного письма для девеломпента / в боевом серваке статус TRue
                    )
                return HttpResponseRedirect(reverse_lazy('orders:list_order'))


class MyListOrderView(ListView):
    model = models.Order
    template_name = 'orders/list_order.html'
    paginate_by = 30

    def get_queryset(self):
        username = self.request.user.get_username()
        order = models.Order.objects.filter(contact_info=username)
        #queryset = super().get_queryset()
        queryset = order
        return queryset



