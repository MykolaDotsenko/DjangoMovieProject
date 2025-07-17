from django.urls import path
from .views import *

app_name = "imdb"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('movie/list/', MovieListView.as_view(), name="movie-list"),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name="movie-detail"),
    path('genre/<int:pk>/', GenreDetailView.as_view(), name="genre-detail"),
    path('person/list/', PersonListView.as_view(), name="person-list"),
    path('person/<int:pk>/', PersonDetailView.as_view(), name="person-detail"),
]