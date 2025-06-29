from rest_framework import serializers
from .models import *


class PersonSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = ProgrammingLanguage
        fields = ('id', 'name', 'rating', 'create_date', 'wiki_link', 'logo', 'creator')

class ProjectListSerializer(serializers.ModelSerializer):
    languages = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'languages', 'start_date', 'deadline_date')