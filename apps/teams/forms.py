from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# 2) formularz do dodawania członka zespołu
class AddMemberForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)

    # tech4: walidacja clean() - czy użytkownik już jest w zespole
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user_to_add = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("Użytkownik o takim loginie nie istnieje.")
        
        # tech4: nie można dodać kogoś, kto już tam jest
        if self.team and self.team.members.filter(id=user_to_add.id).exists():
            raise ValidationError(f"Użytkownik {username} jest już członkiem tego zespołu!")
        
        return user_to_add