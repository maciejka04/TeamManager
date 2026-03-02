from django import forms
from django.contrib.auth.models import User

from .models import Profile


# 1) Edycja danych (ModelForm dla User)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# 1) profil - edycja "o mnie" i avatara
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']