from django.contrib import admin
from django.utils.html import format_html_join

from .models import Genre, Movie, Participation, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "birth_date", "movie_list", "role_list")
    list_filter = ("gender",)
    search_fields = ("first_name", "last_name")
    ordering = ("first_name", "last_name")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("credits__movie")

    @admin.display(ordering="first_name", description="Name")
    def name(self, obj):
        return str(obj)

    @admin.display(description="Movies")
    def movie_list(self, obj):
        return format_html_join(
            "",
            "{}<br>",
            ((credit.movie.title,) for credit in obj.credits.all()),
        )

    @admin.display(description="Roles")
    def role_list(self, obj):
        return format_html_join(
            "",
            "{}<br>",
            ((credit.get_role_display(),) for credit in obj.credits.all()),
        )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "rating", "release_date", "genres_str")
    list_filter = ("age_rating", "genres")
    search_fields = ("title",)
    ordering = ("title",)
    filter_horizontal = ("genres",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("genres")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("movie", "person", "role")
    list_filter = ("role",)
    list_select_related = ("movie", "person")
    search_fields = ("movie__title", "person__first_name", "person__last_name")
    ordering = ("movie__title", "person__last_name")
