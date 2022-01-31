from django.shortcuts import render

# Create your views here.

from . models import Author, Serie, Genre, Editor

def author_list(request):
    author = Author.objects.all()
    ctx = {
        'author' : author
    }
    return render(request, template_name='authors_list.html', context=ctx)

def author_detail(request, author_id):
    author_data = Author.objects.get(pk=author_id)
    ctx = {
        'author_data' : author_data
    }
    return render(request, template_name='author_detail.html', context=ctx)

def serie_list(request):
    serie = Serie.objects.all()
    ctx = {
        'serie' : serie
    }
    return render(request, template_name='serie_list.html', context=ctx)

def serie_detail(request, serie_id):
    serie_data = Serie.objects.get(pk=serie_id)
    ctx = {
        'serie_data' : serie_data
    }
    return render(request, template_name='serie_detail.html', context=ctx)


def genre_list(request):
    genre = Genre.objects.all()
    ctx = {
        'genre' : genre
    }
    return render(request, template_name='genre_list.html', context=ctx)

def genre_detail(request, genre_id):
    genre_data = Genre.objects.get(pk=genre_id)
    ctx = {
        'genre_data' : genre_data
    }
    return render(request, template_name='genre_detail.html', context=ctx)


def editor_list(request):
    editor = Editor.objects.all()
    ctx = {
        'editor' : editor
    }
    return render(request, template_name='editor_list.html', context=ctx)

def editor_detail(request, editor_id):
    editor = Editor.objects.get(pk=editor_id)
    ctx = {
        'editor_data' : editor
    }
    return render(request, template_name='editor_detail.html', context=ctx)