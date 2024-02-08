from django.urls import path
from .views import GenreView, MovieDetailView, MovieListView

urlpatterns = [
    path('genres/', GenreView.as_view()),
    path('movie/<int:movie_id>/', MovieDetailView.as_view()),
    path('movies/', MovieListView.as_view()),

]
