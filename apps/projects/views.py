from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from apps.teams.models import Team

from .forms import ProjectForm, TaskForm
from .models import Comment, Project, Task


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm 
    template_name = 'projects/project_form.html'

    def get_form_kwargs(self):
        """Przekazuje zespół do formularza, aby metoda clean_name mogła go użyć."""
        kwargs = super().get_form_kwargs()

        team = get_object_or_404(Team, id=self.kwargs['team_id'], members=self.request.user)
        kwargs['team'] = team
        return kwargs

    def form_valid(self, form):
        form.instance.team = get_object_or_404(Team, id=self.kwargs['team_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('team_detail', kwargs={'pk': self.object.team.id})

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    # tech2: OPTYMALIZACJA: prefetch_related zapobiega problemowi N+1 przy pobieraniu członków zespołu
    def get_object(self, queryset=None):
        queryset = Project.objects.prefetch_related('team__members')
        project = super().get_object(queryset)
        # 2) izolacja danych - blokada dostepu dla osób spoza zespolu
        if self.request.user not in project.team.members.all():
            raise PermissionDenied("Nie masz dostępu do tego projektu.")
        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # tech2: OPTYMALIZACJA: select_related pobiera dane użytkownika jednym zapytaniem SQL JOIN
        tasks_base = self.object.tasks.select_related('assigned_to', 'assigned_to__profile')
        # 3) widok Kanban (podzial zadan na kolumny)
        context['todo_tasks'] = tasks_base.filter(status='TODO')
        context['in_progress_tasks'] = tasks_base.filter(status='IN_PROGRESS')
        context['done_tasks'] = tasks_base.filter(status='DONE')
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        kwargs['team'] = project.team 
        return kwargs

    def form_valid(self, form):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['project_id']})

# 3) latwy sposób na zmianę statusu (Przycisk "Przesuń dalej")
def move_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user not in task.project.team.members.all():
        raise PermissionDenied
    # 3) logika szybkiego przesuwania zadania w Kanbanie
    if task.status == 'TODO':
        task.status = 'IN_PROGRESS'
    elif task.status == 'IN_PROGRESS':
        task.status = 'DONE'
    
    task.save()
    return redirect('project_detail', pk=task.project.id)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'projects/task_detail.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        queryset = Task.objects.select_related('project__team').prefetch_related(
            'comments__author__profile', 
            'project__team__members' 
        )
        task = super().get_object(queryset)
        
        if self.request.user not in task.project.team.members.all():
            raise PermissionDenied("Nie masz dostępu do tego zadania.")
        return task

# 4) obsluga dodawania komentarza
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.user not in task.project.team.members.all():
        raise PermissionDenied

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                task=task,
                author=request.user,
                content=content
            )
            messages.success(request, "Komentarz został dodany.")
    
    return redirect('task_detail', pk=task.id)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'  

    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if self.request.user not in task.project.team.members.all():
            raise PermissionDenied
        return task

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['team'] = self.object.project.team
        return kwargs

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.id})

# 5) dashboard osobisty - centrum dowodzenia uzytkownika
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # 5) lista zespolow i prefetch dla optymalizacji
        context['user_teams'] = Team.objects.filter(members=user).prefetch_related('members')
        # 5) sekcja "Moje pilne zadania" - zadania przypisane do mnie, ktore nie sa jeszcze zakonczone
        context['my_tasks'] = Task.objects.select_related(
            'project', 
            'assigned_to__profile'
        ).filter(
            assigned_to=user
        ).exclude(status='DONE').order_by('due_date', 'priority')
        
        return context