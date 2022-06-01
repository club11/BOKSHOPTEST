from dataclasses import field, fields
from pyexpat import model
from re import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#from airplanes import models

# Create your views here.

from . import models
from . import forms
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView


class DirectoriesTemplateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'directories/directories.html'
    login_url = reverse_lazy('profiles:login')
    permission_required = ('directories.view_author', )

    def  get_context_data(self, **kwargs):                              #Типовой пример расширения функционала view:
        #list_a = models.Author.objects.all()                        #list_a = models.Author.objects.all()
        #list_b = models.Editor.objects.all()                        #list_b = models.Editor.objects.all()                    
        context = super().get_context_data(**kwargs)                    #context = super().get_context_data(**kwargs)
        #context['list_a'] = list_a                                      #context['list_a'] = list_a 
        #context['list_b'] = list_b                                      #context['list_b'] = list_b 
        return context                                                  #return context      

class AuthorListView(LoginRequiredMixin, ListView):
    model = models.Author
    login_url = reverse_lazy('profiles:login')

    #permission_required = 'Can view author'

    def get_queryset(self):                                     # еще один типовой пример
        qs = super().get_queryset()                             # доработка qeryseta
        #return qs.filter(pk__lt=5)                             # фильтруем
        #print(self.request.user)                                #a вот еще ФИШКА REQUEST
        #print(self.request.POST)                                # надо поизучать 
        #print(self.request.GET)  
        return qs
class AuthorDetailView(LoginRequiredMixin,DetailView):
    model = models.Author
    template = 'author_detail.html'
    login_url = reverse_lazy('profiles:login')

class AuthorCreateView(LoginRequiredMixin,CreateView):
    model = models.Author
    form_class = forms.AuthorCreateForm
    login_url = reverse_lazy('profiles:login')
    # либо прописать просто поля модельной формы:
    #fields = [
    #    'author',
    #]

class AuthorUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Author
    form_class = forms.AuthorCreateForm
    login_url = reverse_lazy('profiles:login')

class AuthorDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Author
    success_url = reverse_lazy('directories:author_list')
    login_url = reverse_lazy('profiles:login')

##############################################################################################################
class EditorListView(LoginRequiredMixin,ListView):
    model = models.Editor
    login_url = reverse_lazy('profiles:login')
class EditorDetailView(LoginRequiredMixin,DetailView):
    model = models.Editor
    login_url = reverse_lazy('profiles:login')

class EditorCreateview(LoginRequiredMixin,CreateView):
    model = models.Editor
    form_class = forms.EditorCreateForm
    login_url = reverse_lazy('profiles:login')
class EditorUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Editor
    form_class = forms.EditorCreateForm
    login_url = reverse_lazy('profiles:login')
class EditorDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Editor
    success_url = reverse_lazy('directories:editor_list')
    login_url = reverse_lazy('profiles:login')

class SerieListview(LoginRequiredMixin,ListView):
    model = models.Serie
    login_url = reverse_lazy('profiles:login')

class SerieDetailView(LoginRequiredMixin,DetailView):
    model = models.Serie
    login_url = reverse_lazy('profiles:login')
class SerieCreateView(LoginRequiredMixin,CreateView):
    model = models.Serie
    form_class = forms.SerieCreateForm
    login_url = reverse_lazy('profiles:login')
class SerieUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Serie
    form_class = forms.SerieCreateForm
    login_url = reverse_lazy('profiles:login')
class SerieDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Serie
    success_url = reverse_lazy('directories:series_list')
    login_url = reverse_lazy('profiles:login')

class GenreListView(LoginRequiredMixin,ListView):
    model = models.Genre
    login_url = reverse_lazy('profiles:login')

class GenreDetailView(LoginRequiredMixin,DetailView):
    model = models.Genre  
    login_url = reverse_lazy('profiles:login')
class GenreCreateView(LoginRequiredMixin,CreateView):
    model = models.Genre  
    form_class = forms.GenreCreateForm
    login_url = reverse_lazy('profiles:login')
class GenreUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Genre  
    form_class = forms.GenreCreateForm
    login_url = reverse_lazy('profiles:login')
class GenreDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Genre
    success_url = reverse_lazy('directories:genre_list')
    login_url = reverse_lazy('profiles:login')





#def editor_list(request):
#    editor = Editor.objects.all()
#    ctx = {
#        'editor' : editor
#    }
#    return render(request, template_name='editor_list.html', context=ctx)

#def editor_detail(request, editor_id):
#    editor = Editor.objects.get(pk=editor_id)
#    ctx = {
#        'editor_data' : editor
#    }
#    return render(request, template_name='editor_detail.html', context=ctx)

#def editor_create(request):
#    if request.method =="POST":
#        form = forms.EditorCreateForm(request.POST)
#        if form.is_valid():
#            editor = form.cleaned_data.get('editor')         
#            form.save()  
#            return HttpResponseRedirect(reverse('editor_list'))
#        else:
#            pass
#    else:
#        ctx = {
#            'form' : forms.EditorCreateForm()
#        }
#    return render(request, template_name='editor_create.html', context=ctx)

#def editor_update(request, editor_id):
#    if request.method == "POST":
#        obj = Editor.objects.get(pk=editor_id)
#        form = forms.EditorCreateForm(request.POST,instance=obj)
#        if form.is_valid():
#            editor = form.cleaned_data.get('editor') 
#            form.save()  
#            return HttpResponseRedirect(reverse('editor_list'))
#        else:
#            pass
#    else:
#        obj = Editor.objects.get(pk=editor_id)
#        form = forms.EditorCreateForm(instance=obj)
#    ctx = {
#        'form' : form
#    }
#    return render(request, template_name='editor_update.html', context=ctx) 


#def editor_delete(request, editor_id):
#    if request.method == "POST":
#        obj = Editor.objects.get(pk=editor_id).delete()        
#        return HttpResponseRedirect(reverse('editor_list'))
#    return render(request, template_name='editor_delete.html', context={}) 


#def directories_view(request):
#    return render(request, template_name='directories.html', context={})



#create view for forms
#def author_create(request): 
#    if request.method == "POST":
#        form = forms.AuthorCreateForm(request.POST)
#        print(form.is_valid)
#        if form.is_valid():
#            author = form.cleaned_data.get('author')
#            form.save()                     # сохранить в БД
#            #obj = Author.objects.create(author=author) # или так сохранить в БД
#            return HttpResponseRedirect(reverse('authors_list'))
#        else:
#            pass
#    else:
#        form = forms.AuthorCreateForm()
#    ctx = {    
#        'form' : form,
#        "is_valid" : form.is_valid()
#    }
#    return render(request, template_name='author_create.html', context=ctx)

##update view for forms
#def author_update(request, author_id): 
#    if request.method == "POST":
#        obj = Author.objects.get(pk=author_id)      # хотя вроде и так работает без него сохраняетв бд
#        form = forms.AuthorCreateForm(request.POST, instance=obj)           # вроде и так работает без instance=obj) 
#        print(form.is_valid)
#        if form.is_valid():
#            author = form.cleaned_data.get('author')
#            form.save()                     # сохранить в БД
#            return HttpResponseRedirect(reverse('authors_list'))
#        else:
#            pass
#    else:
#        obj = Author.objects.get(pk=author_id)
#        form = forms.AuthorCreateForm(instance=obj)         #показать заполненную форму
#    ctx = {    
#        'form' : form,
#        "is_valid" : form.is_valid()
#    }
#    return render(request, template_name='author_create.html', context=ctx)

#delete view for forms
#def author_delete(request, author_id): 
#    if request.method == "POST":  
#        obj = Author.objects.get(pk=author_id).delete()
#        return HttpResponseRedirect(reverse('authors_list'))
#    return render(request, template_name='author_delete.html', context={})


##list view
#def author_list(request):
#    author = Author.objects.all()
#    ctx = {
#        'author' : author
#    }
#    return render(request, template_name='authors_list.html', context=ctx)
#detail view
#def author_detail(request, author_id):
#    author_data = Author.objects.get(pk=author_id)
#    ctx = {
#        'author_data' : author_data
#    }
#    return render(request, template_name='author_detail.html', context=ctx)


#def serie_list(request):
#    serie = Serie.objects.all()
#    ctx = {
#        'serie' : serie
#    }
#    return render(request, template_name='serie_list.html', context=ctx)

#def serie_detail(request, serie_id):
#    serie_data = Serie.objects.get(pk=serie_id)
#    ctx = {
#        'serie_data' : serie_data
#    }
#    return render(request, template_name='serie_detail.html', context=ctx)

#def serie_create(request):
#    if request.method == 'POST':
#        form = forms.SerieCreateForm(request.POST)
#        if form.is_valid():
#            serie = form.cleaned_data.get('serie')
#            form.save()
#            return HttpResponseRedirect(reverse('series_list'))
#        else:
#            pass
#    else:
#        form = forms.SerieCreateForm()
#    ctx = {
#        'form' : form,
#        "is_valid" : form.is_valid(),
#    }
#    return render(request, template_name='serie_create.html', context=ctx)


#def serie_update(request, serie_id):
#    if request.method == "POST":
#        obj = Serie.objects.get(pk=serie_id)
#        form = forms.SerieCreateForm(request.POST, instance=obj)
#        if form.is_valid():
#            serie = form.cleaned_data.get('serie')
#            form.save()
#            return HttpResponseRedirect(reverse('series_list'))
#    else:
#        obj = Serie.objects.get(pk=serie_id)
#        form = forms.SerieCreateForm(instance=obj)
#    ctx = {
#        'form' : form,
#        "is_valid" : form.is_valid(),
#    }
#    return render(request, template_name='serie_update.html', context=ctx)


#def serie_delete(request, serie_id):
#    if request.method == "POST":
#        obj = Serie.objects.get(pk=serie_id).delete()
#        return HttpResponseRedirect(reverse('series_list'))
#    return render(request, template_name='serie_delete.html', context={})



#def genre_list(request):
#    genre = Genre.objects.all()
#    ctx = {
#        'genre' : genre
#    }
#    return render(request, template_name='genre_list.html', context=ctx)

#def genre_detail(request, genre_id):
#    genre_data = Genre.objects.get(pk=genre_id)
#    ctx = {
#        'genre_data' : genre_data
#    }
#    return render(request, template_name='genre_detail.html', context=ctx)

#def genre_create(request):
#    if request.method == 'POST':
#        form = forms.GenreCreateForm(request.POST)
#        if form.is_valid():
#            genre = form.cleaned_data.get('genre')
#            form.save()
#            return HttpResponseRedirect(reverse('genre_list'))
#        else:
#            pass
#    else:
#        ctx = {
#            'form' : forms.GenreCreateForm() 
#        }
#    return render(request, template_name='genre_create.html', context=ctx)

#def genre_update(request, genre_id):
#    if request.method == "POST":
#        obj= Genre.objects.get(pk=genre_id)
#        form = forms.GenreCreateForm(request.POST,instance=obj) 
#        if form.is_valid():
#            genre = form.cleaned_data.get('genre')
#            form.save()
#            return HttpResponseRedirect(reverse('genre_list'))
#        else:
#            pass
#    else:
#        obj= Genre.objects.get(pk=genre_id)
#        form = forms.GenreCreateForm(instance=obj) 
#        ctx = {
#            'form' : form,
#        }
#    return render(request, template_name='genre_update.html', context=ctx)


#def genre_delete(request, genre_id):
#    if request.method == "POST":
#        obj = Genre.objects.get(pk = genre_id).delete()
#        return HttpResponseRedirect(reverse('genre_list'))
#    return render(request, template_name='genre_delete.html', context={})