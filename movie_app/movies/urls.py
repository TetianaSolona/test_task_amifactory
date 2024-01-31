from django.urls import path
from .views import genre_list, movie_detail, movie_list

urlpatterns = [
    path('genres/', genre_list, name='genre-list'),
    path('movie/<int:movie_id>/', movie_detail, name='movie-detail'),
    path('movies/', movie_list, name='movie-list'),

]
