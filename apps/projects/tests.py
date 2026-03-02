import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.teams.models import Team

from .forms import ProjectForm, TaskForm
from .models import Project

# tech6: testy automatyczne

class ProjectSecurityAndValidationTest(TestCase):
    def setUp(self):
        self.ania = User.objects.create_user(username='ania', password='password123')
        self.bartek = User.objects.create_user(username='bartek', password='password123')
        
        self.team_ania = Team.objects.create(name="Team Ani", owner=self.ania)
        self.team_ania.members.add(self.ania)
        self.project_ania = Project.objects.create(name="Tajny Projekt", team=self.team_ania)

    def test_access_isolation_between_teams(self):
        """
        TEST: Czy Bartek (zespół B) dostanie 403 próbując wejść w projekt Ani (zespół A).
        Sprawdza PermissionDenied w get_object.
        """
        self.client.login(username='bartek', password='password123')
        url = reverse('project_detail', kwargs={'pk': self.project_ania.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)

    def test_task_clean_due_date_validation(self):
        """
        TEST: Czy walidacja clean_due_date blokuje daty z przeszłości.
        Sprawdza TaskForm.
        """
        yesterday = timezone.now().date() - datetime.timedelta(days=1)
        form_data = {
            'title': 'Zadanie z przeszłości',
            'due_date': yesterday,
            'status': 'TODO',
            'priority': 'M',
            'assigned_to': self.ania.id
        }

        form = TaskForm(data=form_data, team=self.team_ania)
        
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)
        self.assertEqual(form.errors['due_date'][0], "Data wykonania nie może być z przeszłości!")

    def test_project_name_uniqueness_in_team(self):
        """
        TEST: Czy metoda clean_name blokuje dwa projekty o tej samej nazwie w jednym zespole.
        Sprawdza ProjectForm.
        """
        form_data = {'name': 'Tajny Projekt'} 
        form = ProjectForm(data=form_data, team=self.team_ania)
        
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'][0], "Projekt o tej nazwie już istnieje w Twoim zespole!")