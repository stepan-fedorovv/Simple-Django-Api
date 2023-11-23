from django.db import models
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)


