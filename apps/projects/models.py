from django.contrib.auth.models import User
from django.db import models

from apps.teams.models import Team


class Project(models.Model):
    name = models.CharField(max_length=100)
    # 2) i tech2 - ForeignKey do Team - W RAMACH JEDNEGO ZESPOLU MOZE BYC WIELE PROJEKTOW
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class Task(models.Model):
    # 3) priorytet zadania 
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]
    # 3)status zadania 
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    # 3)tytul i opis zadania
    title = models.CharField(max_length=200, verbose_name="Tytuł zadania")
    description = models.TextField(blank=True, verbose_name="Opis")
    
    priority = models.CharField(
        max_length=1, 
        choices=PRIORITY_CHOICES, 
        default='M', 
        verbose_name="Priorytet"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='TODO', 
        verbose_name="Status"
    )

    # 3) data wykonania zadania
    due_date = models.DateField(null=True, blank=True, verbose_name="Data wykonania")
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )

    # 3) przypisanie zadania do użytkownika
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tasks',
        verbose_name="Przypisane do"
    )

    # 4) zalaczniki do zadania 
    attachment = models.FileField(
        upload_to='task_attachments/', 
        null=True, 
        blank=True, 
        verbose_name="Załącznik"
    )

    class Meta:
        ordering = ['due_date', 'priority']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# 4) mozliwosc dodania komentarzy pod zadaniem
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    # 4) widoczna data
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komentarz {self.author.username} do {self.task.title}"