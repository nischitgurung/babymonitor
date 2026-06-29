from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (

        ("parent", "Parent"),

        ("caregiver", "Caregiver"),

        ("admin", "Admin"),

    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="parent",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username