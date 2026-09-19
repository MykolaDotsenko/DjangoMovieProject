from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db.models import Count, Prefetch, Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import SignInForm, SignUpForm
from .models import Genre, Movie, Participation, Person


class IndexView(TemplateView):
    template_name = "imdb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_movies"] = Movie.objects.order_by("-rating", "title")[:6]
        context["featured_people"] = (
            Person.objects.annotate(credit_count=Count("credits"))
            .order_by("-credit_count", "last_name", "first_name")[:6]
        )
        return context


class MovieListView(ListView):
    model = Movie
    context_object_name = "movies"
    paginate_by = 12

    def get_queryset(self):
        queryset = Movie.objects.order_by("title")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(genres__name__icontains=query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class MovieDetailView(DetailView):
    model = Movie
    context_object_name = "movie"

    def get_queryset(self):
        return Movie.objects.prefetch_related("genres")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        credits = list(
            self.object.credits.select_related("person").order_by(
                "person__last_name",
                "person__first_name",
            )
        )
        context["actors"] = [
            credit.person
            for credit in credits
            if credit.role == Participation.Role.ACTOR
        ]
        context["directors"] = [
            credit.person
            for credit in credits
            if credit.role == Participation.Role.DIRECTOR
        ]
        return context


class GenreDetailView(DetailView):
    model = Genre
    context_object_name = "genre"
    template_name = "imdb/genre.html"

    def get_queryset(self):
        return Genre.objects.prefetch_related(
            Prefetch("movies", queryset=Movie.objects.order_by("title"))
        )


class PersonListView(ListView):
    model = Person
    context_object_name = "people"
    paginate_by = 18

    def get_queryset(self):
        return Person.objects.order_by("last_name", "first_name")


class PersonDetailView(DetailView):
    model = Person
    context_object_name = "person"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["credits"] = self.object.credits.select_related("movie").order_by(
            "-movie__release_date",
            "movie__title",
        )
        context["featured_trailer"] = self.object.get_featured_trailer()
        return context


class SignInView(LoginView):
    template_name = "imdb/authorization.html"
    authentication_form = SignInForm
    redirect_authenticated_user = True


class SignUpView(FormView):
    template_name = "imdb/create_account.html"
    form_class = SignUpForm
    success_url = reverse_lazy("imdb:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Welcome, {user.username}. Your account is ready.")
        return super().form_valid(form)
