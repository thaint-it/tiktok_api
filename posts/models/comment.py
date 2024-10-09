from django.db import models
from posts.models.post import Post
from users.models import User
from base_services.models  import AutoTimeStampedModel

# Create your models here.
class Comment(AutoTimeStampedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, null=True,on_delete=models.DO_NOTHING)  # Added max_length
    content = models.CharField(max_length=500, null=True)  # Added max_length
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    class Meta:
        db_table = "comments"
