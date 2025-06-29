from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'create_date', 'creator')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'deadline_date')