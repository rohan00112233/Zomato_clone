from django.contrib.auth.models import AbstractUser
from django.db import models    

class User(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)