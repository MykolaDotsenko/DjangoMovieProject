from django.contrib import admin
from django.utils.html import format_html_join

from .models import Genre, Movie, Participation, Person, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar")
    search_fields = ("user__username",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "birth_date", "movie_list", "role_list")
    list_filter = ("gender",)
    search_fields = ("first_name", "last_name")
    ordering = ("first_name", "last_name")

    @admin.display(ordering="first_name", description="Name")
    def name(self, obj):
        return str(obj)

    @admin.display(description="Movies")
    def movie_list(self, obj):
        return format_html_join(
            "",
            "{}<br>",
            ((participation.movie.title,) for participation in obj.participation_set.all()),
        )

    @admin.display(description="Roles")
    def role_list(self, obj):
        return format_html_join(
            "",
            "{}<br>",
            (
                (participation.get_role_display(),)
                for participation in obj.participation_set.all()
            ),
        )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "rating", "release_date", "genres_str")
    list_filter = ("age_rating", "genres")
    search_fields = ("title",)
    ordering = ("title",)
    filter_horizontal = ("genres",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("movie", "person", "role")
    list_filter = ("role",)
    search_fields = ("movie__title", "person__first_name", "person__last_name")
    ordering = ("movie__title", "person__last_name")
