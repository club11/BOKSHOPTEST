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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import carts # для картинок в dev режиме


urlpatterns = [
    path('admin/', admin.site.urls),
    path('directory/', include('directories.urls', namespace='directories')),               #включаем модуль 'directories.urls' gпод неймингом/пространством имен 'directories'. иерархия urls путем Inclde
    path('', include('books.urls', namespace='books')),
    path('cart/', include('carts.urls', namespace='carts')), 
    path('order/', include('orders.urls', namespace='orders')), 
    path('profiles/', include('profiles.urls', namespace='profiles')), 
    path('comments/', include('comments.urls', namespace='comments')), 
    path('staff/', include('staff.urls', namespace='staff')), 
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#from airplanes import views as airplanes_codes_view

    #path('flat/<int:flat_id>/', airplanes_codes_view.flat_detail, name='flat'),
    #path('flats/', airplanes_codes_view.flat_list, name = 'flat_list'),

    #path('<airport>/', airplanes_codes_view.code_to_airport),
    #path('', airplanes_codes_view.homepage),

#    path('editor_detail/<int:editor_id>/', directories_views.editor_detail, name='editors'),
#    path('editors/', directories_views.editor_list, name='editor_list'),
#    path('editor_create/', directories_views.editor_create, name='editor_create'),
#    path('editor_update/<int:editor_id>', directories_views.editor_update, name='editor_update'),
#    path('editor_delete/<int:editor_id>', directories_views.editor_delete, name='editor_delete'),