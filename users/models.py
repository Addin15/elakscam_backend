from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    password = models.TextField()
    premium = models.BooleanField(default=False)
    credibility = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
