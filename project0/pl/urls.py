from django.urls import path
from .views import *

app_name = "pl"
urlpatterns = [
    # path('index/', index, name='index'),
    path('index/', IndexView.as_view(), name="index"),
    path('language/<int:pk>/', ProgrammingLanguageDetailView.as_view(), name="pl-detail-view"),
    path('person/<int:pk>/', PersonDetailView.as_view(), name="person-detail-view"),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project-detail-view"),
    path('update/rating/', update_rating, name="update-rating"),
    path('update/person/', update_person, name="update-person"),
    path('create/project/', add_new_project, name="add-new-project"),

    path('api/person/list/', PersonListAPIView.as_view()),
    path('api/person/<int:pk>/', PersonRetrieveAPIView.as_view()),

    path('api/lang/list/', ProgrammingLanguageListAPIView.as_view()),
    path('api/project/list/', ProjectListAPIView.as_view()),
    ]