from django.contrib import admin
from .models import *

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'gender', 'birth_date', "portrait")

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'genres_str')
    

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display= ('name',)

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('movie', 'person', 'role')

# Register your models here.
