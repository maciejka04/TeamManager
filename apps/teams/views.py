from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import AddMemberForm
from .models import Team


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    fields = ['name']
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('team_list')

    # 2) użytkownik automatycznie staje się właścicielem
    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        # 2) automatyczne dodanie właściciela do członków
        form.instance.members.add(self.request.user)
        return response

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    # 2) izolacja - widzisz tylko te zespoly do ktorych nalezysz
    def get_queryset(self):
        return Team.objects.filter(members=self.request.user)

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    # 2) izolacja - blad 403 (PermissionDenied) przy probie wejscia w nie swoj zespol
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user not in obj.members.all():
            raise PermissionDenied("Nie należysz do tego zespołu.")
        return obj

# 2) dodawanie członka przez właściciela
def add_team_member(request, team_id):
    # 2) tylko owner może dodać kogoś (filtr owner=request.user)
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    
    if request.method == 'POST':
        form = AddMemberForm(request.POST, team=team)
        
        if form.is_valid():
            user_to_add = form.cleaned_data.get('username')
            team.members.add(user_to_add)
            messages.success(request, f"Dodano użytkownika {user_to_add.username}.")
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    
    return redirect('team_detail', pk=team_id)