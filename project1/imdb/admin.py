from django.contrib import admin
from .models import *

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'gender', 'birth_date', "portrait")

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('__str__', )



# Register your models here.
