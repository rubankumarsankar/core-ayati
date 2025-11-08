from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    # Link to Role table (role-based access)
    role = models.ForeignKey(
        Role,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )

    def __str__(self):
        return f"{self.username} ({self.role.name if self.role else 'No Role'})"
