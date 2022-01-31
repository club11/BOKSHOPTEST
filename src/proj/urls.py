"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path

from airplanes import views as airplanes_codes_view
from directories import views as directories_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('flat/<int:flat_id>/', airplanes_codes_view.flat_detail, name='flat'),
    path('flats/', airplanes_codes_view.flat_list, name = 'flat_list'),

    path('author_detail/<int:author_id>/', directories_views.author_detail, name='authors'),
    path('authors/', directories_views.author_list, name='authors_list'),

    path('serie_detail/<int:serie_id>/', directories_views.serie_detail, name='series'),
    path('series/', directories_views.serie_list, name='series_list'),

    path('genre_detail/<int:genre_id>/', directories_views.genre_detail, name='genres'),
    path('genres/', directories_views.genre_list, name='genre_list'),

    path('editor_detail/<int:editor_id>/', directories_views.editor_detail, name='editors'),
    path('editors/', directories_views.editor_list, name='editor_list'),

    path('<airport>/', airplanes_codes_view.code_to_airport),
    path('', airplanes_codes_view.homepage),
]


