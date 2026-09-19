from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import (
    GenreDetailView,
    IndexView,
    MovieDetailView,
    MovieListView,
    PersonDetailView,
    PersonListView,
    SignInView,
    SignUpView,
)

app_name = "imdb"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("genres/<int:pk>/", GenreDetailView.as_view(), name="genre-detail"),
    path("people/", PersonListView.as_view(), name="person-list"),
    path("people/<int:pk>/", PersonDetailView.as_view(), name="person-detail"),
    path("auth/login/", SignInView.as_view(), name="login"),
    path("auth/signup/", SignUpView.as_view(), name="signup"),
    path(
        "auth/logout/",
        LogoutView.as_view(next_page=reverse_lazy("imdb:index")),
        name="logout",
    ),
]
