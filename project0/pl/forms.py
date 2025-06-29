from django.forms import ModelForm, DateInput
from .models import *


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'deadline_date': DateInput(attrs={'type': 'date'}),
        }

