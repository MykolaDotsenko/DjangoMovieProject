from django.contrib import admin
from .models import *
from django.utils.html import format_html
from embed_video.admin import AdminVideoMixin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'gender', 'birth_date', "portrait", 'movie_list', 'role_list')
    ordering = ['first_name']

    def movie_list(self, obj):
        titles = [p.movie.title for p in obj.participation_set.all()]
        return format_html('<br>'.join(titles))
    movie_list.short_description = "Movies"

    def role_list(self, obj):
        roles = [p.get_role_display() for p in obj.participation_set.all()]
        return format_html('<br>'.join(roles))
    role_list.short_description = "Roles"

    @admin.display(ordering='first_name', description='Name')
    def __str__(self, obj):
        return str(obj)


@admin.register(Movie)
class MovieAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('__str__', 'genres_str')
    ordering = ['title']
    

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display= ('name',)

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('movie', 'person', 'role')
    ordering = ['movie__title']

# Register your models here.
