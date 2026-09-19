from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from .forms import *

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
 

def user_sign_out(request):
    logout(request)
    return redirect('imdb:index')

class AuthorizationView(TemplateView):
    template_name = 'imdb/authorization.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AuthorizationForm()
        return context
    
    def post(self, request):
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.add_message(request, messages.INFO, "Wrong username or password")

        return redirect('imdb:index')


class CreateAccountView(TemplateView):
    template_name = 'imdb/create_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateAccountForm()
        return context
    
    def post(self, request):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.INFO, "Username already exists")
            return redirect('imdb:create-account-view')
        elif password1 != password2:
            messages.add_message(request, messages.INFO, "Passwords dont match")
            return redirect('imdb:create-account-view')           
        else:
            return redirect('imdb:index')