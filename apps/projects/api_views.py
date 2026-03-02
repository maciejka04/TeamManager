from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, Task
from .serializers import TaskSerializer


class MyTaskViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    6) GET /api/my-tasks/?status=todo
    Endpoint zwraca listę zadań przypisanych do zalogowanego użytkownika
    """
    serializer_class = TaskSerializer

    # 6) dokumentacja Swagger - parametr filtrowania
    @extend_schema(
        parameters=[
            OpenApiParameter(name='status', description='Status (todo, in_progress, done)', required=False, type=str),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        # 6) uwierzytelnienie JWT zapewnia ze self.request.user jest zalogowanym uzytkownikiem
        user = self.request.user
        # tech2: OPTYMALIZACJA: select_related
        queryset = Task.objects.select_related('project', 'assigned_to').filter(assigned_to=user)
        # 6) mozliwosc filtrowania po statusie
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param.upper())
        return queryset

class ProjectStatsViewSet(viewsets.GenericViewSet):
    """
    6) GET /api/projects/{id}/stats/
    Endpoint zwraca statystyki konkretnego projektu.
    """
    # tech2: OPTYMALIZACJA: prefetch_related
    queryset = Project.objects.prefetch_related('tasks').all()
    serializer_class = TaskSerializer
    # 6) akcja niestandardowa - statystyki dostępne pod konkretnym ID projektu
    @action(detail=True, methods=['get'], url_path='stats')
   
    def stats(self, request, pk=None):
        project = self.get_object()
        # 6) liczenie zadan ogołem i zakonczonych
        total_tasks = project.tasks.count()
        done_tasks = project.tasks.filter(status='DONE').count()
        
        # 6) odpowiedz w formacie JSON
        return Response({
            'project_name': project.name,
            'total_tasks': total_tasks,
            'done_tasks': done_tasks,
            'completion_percentage': (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
        })