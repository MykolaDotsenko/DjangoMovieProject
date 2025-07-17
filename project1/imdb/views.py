from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import *


class IndexView(TemplateView):
    template_name = "imdb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_list'] = Movie.objects.order_by('?')[:6]
        context['person_list'] = Person.objects.order_by('?')[:6]
        
        return context


class MovieListView(ListView):
    # model = Movie
    queryset = Movie.objects.order_by("title")

class MovieDetailView(DetailView):
    model = Movie

class GenreDetailView(DetailView):
    model = Genre
    template_name = "imdb/genre.html"

class PersonListView(ListView):
    model = Person
    queryset = Person.objects.order_by("last_name", "first_name")

class PersonDetailView(DetailView):
    model = Person
 