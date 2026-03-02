from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)

    # tech4: customowa walidacja w metodzie clean() - unikalnosc nazwy projektu w zespole
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.team and Project.objects.filter(team=self.team, name=name).exists():
            raise ValidationError("Projekt o tej nazwie już istnieje w Twoim zespole!")
        return name

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date', 'assigned_to', 'attachment']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        # 3) przypisanie do zadania ograniczone tylko do czlonkow danego zespołu
        if team:
            self.fields['assigned_to'].queryset = team.members.all()
            self.fields['assigned_to'].label_from_instance = lambda obj: f"{obj.username}"
    # tech4: customowa walidacja - data nie moze byc z przeszlosci
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise ValidationError("Data wykonania nie może być z przeszłości!")
        return due_date