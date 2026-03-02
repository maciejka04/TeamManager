from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.projects.api_views import MyTaskViewSet, ProjectStatsViewSet
from apps.projects.views import (
    DashboardView,
    ProjectCreateView,
    ProjectDetailView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    add_comment,
    move_task,
)
from apps.teams.views import TeamCreateView, TeamDetailView, TeamListView, add_team_member
from apps.users.views import UserCreateView, home_view, profile_view

# tech5: rejestracja routera: automatyzuje proces tworzenia sciezek URL dla API
router = DefaultRouter()
router.register(r'my-tasks', MyTaskViewSet, basename='my-tasks')
router.register(r'projects', ProjectStatsViewSet, basename='projects')

urlpatterns = [
    path("", home_view, name="home"),
    # 5) dashboard osobisty
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("admin/", admin.site.urls),
    
    # 1) rejestracja i profil
    path("register/", UserCreateView.as_view(), name="register"),
    path("profile/", profile_view, name="profile"),

    # 1) standardowy mechanizm uwierzytelniania 
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # 1) reset hasła: mechanizm odzyskiwania hasla
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),

     # 2) Struktura Organizacyjna - zespoly
    path('teams/', TeamListView.as_view(), name='team_list'),
    path('teams/new/', TeamCreateView.as_view(), name='team_create'),
    # 2) dodawanie czlonka do zespolu
    path('teams/<int:team_id>/add-member/', add_team_member, name='add_team_member'),
    path('teams/<int:team_id>/new-project/', ProjectCreateView.as_view(), name='project_create'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
     # 3) Kanban
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),

    path('teams/<int:team_id>/projects/new/', ProjectCreateView.as_view(), name='project_create'),

    path('projects/<int:project_id>/tasks/new/', TaskCreateView.as_view(), name='task_create'),
    
    # 3) latwy sposób na zmianę statusu
    path('tasks/<int:task_id>/move/', move_task, name='move_task'),

     # 4) szczegoly zadania
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:task_id>/comment/', add_comment, name='add_comment'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),

     # 6) API - uwierzytelnianie JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),

    # tech5: automatyczna dokumentacja Swagger (drf-spectacular)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]

# tech1: obsluga mediow
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)