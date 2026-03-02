from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ProfileUpdateForm, UserUpdateForm


# 1) rejestracja (uzycie UserCreationForm)
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

# 1) dostep tylko dla zalogowanych uzytkownikow (@login_required)
@login_required
def profile_view(request):
    if request.method == 'POST':
        # 1) Edycja danych i avatara
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Twój profil został zaktualizowany!")
            return redirect('dashboard') 
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

def home_view(request):
    return render(request, 'home.html')