from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.safestring import mark_safe


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"
    class Meta:
        verbose_name_plural = "Users"
        db_table = "users"





