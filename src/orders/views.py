from audioop import reverse
from django.shortcuts import render

import books
from books import models
from . import models 
from . models import carts_models
from . import forms
from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages

class CreateOrderView(FormView):
    form_class = forms.OrderCreateForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('books:home')

    def get_initial(self):                      # подкидывем доп данные в заказ(телефон и прочее из данных ппользователя)
        if self.request.user.is_anonymous:
            return {}
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
        order = models.Order.objects.create(
            cart=cart,
            contact_info=ci,
            order_status = orderstatus
        ) 
        del self.request.session['cart_id']         #чистим сессию bad luck
        #self.request.session.delete('cart_id')    #чистим сессию bad luck / riginal method ain't workin'

        books_in_cart = order.cart.cart.all()               ##### # отправляем сообщение пользователю (подготовка перечня названий книг)
        book_names = []
        for n in range(0, books_in_cart.count()):
            names =books_in_cart[n].book.book_name
            book_names.append(names)    
        book_names_str = ''.join(book_names)
        messages.add_message(self.request, messages.INFO, f'{str(self.request.user)} , Ваш заказ {book_names_str}  принят')            # отправляем сообщение пользователю
        return HttpResponseRedirect(reverse_lazy('carts:cart'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')               #обращаемся к СЕССИИ текущей за корзины id
        cart, created = carts_models.Cart.objects.get_or_create(          #распаковка тапла
            pk=cart_id,                                       # поле по которому производится поиск
            defaults={},
        )       
        context['object'] = cart
        return context 


