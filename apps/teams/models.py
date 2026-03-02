from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    # 2) i tech2 - uzytkownik staje się wlascicielem (relacja OneToMany)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    # 2) i tech 2 -  czlonkostwo (relacja ManyToMany)
    members = models.ManyToManyField(User, related_name='teams_joined')

    def __str__(self):
        return self.name