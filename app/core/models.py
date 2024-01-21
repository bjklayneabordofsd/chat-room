from django.db import models
from django.contrib.auth.models import AbstractUser

class AccountModel(AbstractUser):
   name = models.CharField(max_length=100, null=False, default='default_name')

