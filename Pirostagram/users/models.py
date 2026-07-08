from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    introduction = models.TextField(blank=True)
    name = models.CharField(max_length=50, blank=True)

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
    )

    def __str__(self):
        return self.username