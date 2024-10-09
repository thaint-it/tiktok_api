from django.db import models
from posts.models.post import Post
from users.models import User
from base_services.models import AutoTimeStampedModel


# Create your models here.
class View(AutoTimeStampedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "views"


# Create your models here.
class Like(AutoTimeStampedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "likes"


class Favorite(AutoTimeStampedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "favorites"


class Share(AutoTimeStampedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "shares"


class Activity(AutoTimeStampedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, null=True, on_delete=models.DO_NOTHING)
    action=models.CharField(max_length=100, null=True)
    content=models.CharField(max_length=100, null=True)
    is_read = models.BooleanField(null=True, default=False)

    class Meta:
        db_table = "activities"
        
