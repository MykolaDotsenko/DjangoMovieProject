from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from rest_framework import generics
from .models import *
from .forms import *
from .serializers import *

def index(request):
    # object_list = ['monday', 'tuesday', 'friday']
    object_list = ProgrammingLanguage.objects.all()
    context = {
        'object_list': object_list 
    }
    return render(request=request, template_name='pl/index.html', context=context)

class IndexView(TemplateView):
    template_name='pl/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ProgrammingLanguage.objects.order_by("name")
        context['person_list'] = Person.objects.order_by("name")
        context['project_list'] = Project.objects.order_by("title")
        context['project_form'] = ProjectForm()
        return context

class ProgrammingLanguageDetailView(DetailView):
    model = ProgrammingLanguage

class PersonDetailView(DetailView):
    model = Person

class ProjectDetailView(DetailView):
    model = Project

def update_rating(request):
    # print(request.POST)
    pk = request.POST.get('pk')
    rating = request.POST.get('rating')
    name = request.POST.get('name')
    pl = ProgrammingLanguage.objects.get(id=pk)
    pl.rating = rating
    pl.name = name
    pl.save()
    return redirect('pl:pl-detail-view', pk=pk)


def update_person(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        name = request.POST.get('name')
        wiki_link = request.POST.get('wiki_link')
        birth_date = request.POST.get('birth_date')
        person = Person.objects.get(id=pk)
        person.name = name
        person.wiki_link = wiki_link
        person.birth_date = birth_date 
        person.save()
        return redirect('pl:person-detail-view', pk=pk)
    
def add_new_project(request):
    form = ProjectForm(request.POST)
    new_project = form.save()
    return redirect('pl:index')

class PersonListAPIView(generics.ListAPIView):
    serializer_class = PersonSerializer1
    queryset = Person.objects.order_by('birth_date')

class PersonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PersonSerializer1
    queryset = Person.objects.all()

class ProgrammingLanguageListAPIView(generics.ListAPIView):
    serializer_class = ProgrammingLanguageSerializer
    queryset = ProgrammingLanguage.objects.order_by('name')


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.order_by('-start_date')  