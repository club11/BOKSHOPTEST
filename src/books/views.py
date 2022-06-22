from itertools import count
from pyexpat import model
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Q          #импорт Q-object

from . import models
from . import forms
from django.views.generic import DetailView, CreateView, ListView, DeleteView, UpdateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from carts import models as cart_models

class HomeTemplateView(ListView):
    model = models.Book
    form_class = forms.BookForm
    template_name =  'books/home.html' 

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.reverse().order_by('pk')[:3]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        # last 3 added books got here from filter in get_queryset function on step before
        queryset = super().get_queryset()
        context['recomended'] = queryset.reverse().order_by('price')[ : 3]     
        return context

class BookasGoodsListView(ListView):
    model = models.Book
    template_name =  'books/book_goods_list.html'
    paginate_by = 4

    def get_queryset(self):                                 # поиск по книгам | авторам
        queryset = super().get_queryset()
        q = self.request.GET.get('q')   
        if q:
            queryset = queryset.filter(Q(book_name__icontains=q) | Q(author__author__icontains=q))      # крутой НОРМ способ фильтрации по полю book_name через __icontains=q  ( | - или   & - и) --- author__author_ - поиск по полю связанной foreign таблицы
        #elif self.request.GET.get("sorted"): # выведение книг по названию
        #    queryset = queryset.order_by('book_name')
        return queryset  

class BookDetailView(DetailView):
    model = models.Book
    template = 'book_detail.html'

    #def get_context_data(self, **kwargs):
    #    context =  super().get_context_data(**kwargs)
    #    context['star_form'] = forms.RatingForm()       # нетипичный способ внесения значения формы в контекст. возможно лучше сперва через cleaned data...
    #    return context

class BookCreateView(LoginRequiredMixin,CreateView):
    model = models.Book
    form_class = forms.BookForm
    login_url = reverse_lazy('profiles:login')

class BookDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Book
    success_url = reverse_lazy('books:book_list')
    login_url = reverse_lazy('profiles:login')

class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'books/book_update.html'
    success_url = reverse_lazy('books:book_list')
    login_url = reverse_lazy('profiles:login')

class BookListView(LoginRequiredMixin,ListView):
    model = models.Book
    login_url = reverse_lazy('profiles:login')

    def get_queryset(self):                                 # поиск по книгам | авторам
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(book_name__icontains=q) | Q(author__author__icontains=q))      # крутой НОРМ способ фильтрации по полю book_name через __icontains=q  ( | - или   & - и) --- author__author_ - поиск по полю связанной foreign таблицы
        return queryset  
            
    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        context['search_request'] = q

        #################################################################
        # Выборка книг для удаления в случае если не внесены в заказ:

        #carts_with_books_list = models.Book.objects.prefetch_related('books_in_cart')
        #carts_with_books_list = cart_models.BookInCart.objects.select_related('book')
        #books_not_in_cart.difference(all_books, carts_with_books_list)
        all_books = models.Book.objects.all()
        list_of_books = []
        for i in all_books:                             
            list_of_books.append(i.id)  # список всех книг
        books_in_cart = cart_models.BookInCart.objects.all()
        list_of_books_in_cart = []
        for i in books_in_cart:
            list_of_books_in_cart.append(i.book.id)
        set_of_of_books_in_cart = list(set(list_of_books_in_cart))      # список всех книг в заказах
        books_still_not_in_cart = []
        for i in list_of_books:
            if i not in set_of_of_books_in_cart:
                books_still_not_in_cart.append(i)           
        book_not_in_cart = models.Book.objects.filter(id__in=books_still_not_in_cart) # список всех книг не в заказах
        context ['book_not_in_cart'] = book_not_in_cart
        return context 
    

##############################################################################################
#доработать рейтинг
#class AddStarRaing(View):
#    # добавление рейтинга к книге
#    #def get_client_ip(self, request):
#    def post(self, request):
#        form = forms.RatingForm(request.POST)
#        if form.is_valid():
#            models.Rating.objects.update_or_create(
#                book_id=int(request.POST.get('book')),
#                defaults={'star_id': int(request.pOST.get('star'))}
#            )
#            return HttpResponse(status=201)
#        else:
#            return HttpResponse(status=400)
#################################################################################################
