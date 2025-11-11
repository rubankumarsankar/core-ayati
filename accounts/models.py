from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )

    user_code = models.CharField(
        max_length=10,
        unique=True,
        null=True,       # important
        blank=True,
        editable=False,
    )

    def save(self, *args, **kwargs):
        if not self.user_code:
            prefix = "AW"
            last_user = (
                User.objects
                .filter(user_code__startswith=prefix)
                .exclude(user_code__isnull=True)
                .order_by("id")
                .last()
            )

            if last_user and last_user.user_code[2:].isdigit():
                last_number = int(last_user.user_code[2:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.user_code = f"{prefix}{new_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_code or 'NO-CODE'} - {self.username} ({self.role.name if self.role else 'No Role'})"
