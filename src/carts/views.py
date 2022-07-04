from pyexpat import model
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from . import models
from books import models as books_models
from django.views.generic import DetailView, DeleteView, View, RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class CartView(LoginRequiredMixin,DetailView):
    template_name = 'carts/cart_form.html'
    model = models.Cart
    login_url = reverse_lazy('profiles:login')

    def get_object(self, queryset=None):
        # get cart
        cart_id = self.request.session.get('cart_id')               #обращаемся к СЕССИИ текущей
        cart, created = models.Cart.objects.get_or_create(          #распаковка тапла
        pk=cart_id,                                       # поле по которому производится поиск
        defaults={},
        )
        if created:
            self.request.session['cart_id'] = cart.pk
        # get book_in_cart                                  #товарная позиция
        book_id = self.request.GET.get('book_id')
        if book_id:
            book = books_models.Book.objects.get(pk=int(book_id))
            book_in_cart, book_created = models.BookInCart.objects.get_or_create(             
            cart=cart,                        # поиск по полю таблицы модели BookInCart - cart
            #book__pk=int(book_id)           #book__pk поиск через pk  по полю таблицы модели - фильтр объекта
            book=book,
            defaults={
                'unit_price' : book.price
            },
            )
            if not book_created:
                # если товарная позиция уже есть в корзине
                q = book_in_cart.quantity + 1
                book_in_cart.quantity = q
            else:
                book_in_cart.unit_price = book.price
            book_in_cart.save()
        return cart
class GoodInCartDeleteView(RedirectView):
    model = models.BookInCart
    success_url = reverse_lazy('carts:cart')

    def get_redirect_url(self, *args, **kwargs):
        self.model.objects.get(pk=self.kwargs.get('pk')).delete()     # удаляем объект = книгу заказа из корзины
        return self.success_url                                       # новый способ редиректа!!!!

class CartUpdate(LoginRequiredMixin, View):
    login_url = reverse_lazy('profiles:login')    

    def post(self, request):
        action = self.request.POST.get("submit")                 # для сигнала выбор действия охранить корзину иили сохр и заказ
         # get cart
        cart_id = self.request.session.get('cart_id')               #обращаемся к СЕССИИ текущей
        cart, created = models.Cart.objects.get_or_create(          #распаковка тапла
        pk=cart_id,                                       # поле по которому производится поиск
        defaults={},
        )
        if created:
            self.request.session['cart_id'] = cart.pk
        # получаем дынне из общей формы корзины
        #print(self.request.POST)
        goods = cart.cart.all()
        if goods:
            for key, value in request.POST.items():         #Берем ключ  и раскалываем
                if 'quantityforgood_' in key:
                    pk = key.split('_')[1]            # СПЛИТ по второму элеменнту
                    book = goods.get(pk=pk)
                    book.quantity = int(value)
                    book.save()
        if action == 'save_cart':
            return HttpResponseRedirect(reverse_lazy('carts:cart'))
        elif action == 'create_order':
             return HttpResponseRedirect(reverse_lazy('orders:create_order'))
        #elif action == 'create_order' and book.quantity == None:
        #     return HttpResponseRedirect(reverse_lazy('orders:create_order'))  
        else:
            return HttpResponseRedirect(reverse_lazy('carts:cart'))
