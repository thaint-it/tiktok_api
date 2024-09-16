from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):

    email = models.CharField(max_length=255,unique=True,null=True, blank=True)
    user_id = models.CharField(max_length=20, unique=True)
    birthday = models.DateTimeField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(max_length=255, null=True)

    class Meta:
        db_table = "users"
