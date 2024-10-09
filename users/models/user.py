from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from base_services.models.timestamped import AutoTimeStampedModel


class User(AbstractUser):

    email = models.CharField(max_length=255,unique=True,null=True, blank=True)
    system = models.CharField(max_length=255,null=True, blank=True)
    tiktok_id = models.CharField(max_length=20, unique=True)
    birthday = models.DateTimeField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(max_length=255, null=True)
    is_online = models.BooleanField(null=True, default=False)
    

    class Meta:
        db_table = "users"
        
class Follower(AutoTimeStampedModel):
    follower = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING,related_name='follower')
    following=models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING,related_name='following')
    class Meta:
        db_table = "followers"
        
class FolowerActivity(AutoTimeStampedModel):
    follower = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING,related_name='follower_activity')
    following=models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING,related_name='following_activity')
    is_read = models.BooleanField(null=True, default=False)
    class Meta:
        db_table = "follower_activities"
