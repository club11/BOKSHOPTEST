from django.urls import path

from directories import views as directories_views

app_name = 'directories'  # указываем имя модуля что сами создали: directories в папке templates в пакете directories'
urlpatterns = [   
    path('directories/', directories_views.DirectoriesTemplateView.as_view(), name='directories'),

    path('author_detail/<int:pk>/', directories_views.AuthorDetailView.as_view(), name='author'),
    path('authors/', directories_views.AuthorListView.as_view(), name='author_list'),
    path('author-create/', directories_views.AuthorCreateView.as_view(), name='author_create'),
    path('author-update/<int:pk>', directories_views.AuthorUpdateView.as_view(), name='author_update'),
    path('author-delete/<int:pk>', directories_views.AuthorDeleteView.as_view(), name='author_delete'),

    path('editor_detail/<int:pk>/', directories_views.EditorDetailView.as_view(), name='editor'),
    path('editors/', directories_views.EditorListView.as_view(), name='editor_list'),
    path('editor_create/', directories_views.EditorCreateview.as_view(), name='editor_create'),  
    path('editor_update/<int:pk>', directories_views.EditorUpdateView.as_view(), name='editor_update'),    
    path('editor_delete/<int:pk>', directories_views.EditorDeleteView.as_view(), name='editor_delete'),  

    path('sssssserie_detail/<int:pk>/', directories_views.SerieDetailView.as_view(), name='serie'),
    path('series/', directories_views.SerieListview.as_view(), name='series_list'),
    path('serie_create/', directories_views.SerieCreateView.as_view(), name='serie_create'),
    path('serie_update/<int:pk>', directories_views.SerieUpdateView.as_view(), name='serie_update'),
    path('serie_delete/<int:pk>', directories_views.SerieDeleteView.as_view(), name='serie_delete'),

    path('genre_detail/<int:pk>/', directories_views.GenreDetailView.as_view(), name='genre'),
    path('genres/', directories_views.GenreListView.as_view(), name='genre_list'),
    path('genre_create/', directories_views.GenreCreateView.as_view(), name='genre_create'),
    path('genre_update/<int:pk>', directories_views.GenreUpdateView.as_view(), name='genre_update'),
    path('genre_delete/<int:pk>', directories_views.GenreDeleteView.as_view(), name='genre_delete'),
]