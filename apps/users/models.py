from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 1) bio i avatar
    bio = models.TextField(max_length=500, blank=True, verbose_name="O mnie")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Awatar")

    def __str__(self):
        return f"Profil: {self.user.username}"

# Automatyczne tworzenie profilu przy rejestracji
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()