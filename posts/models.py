# from django.db import models
# from users.models import User

# # Create your models here.
# class Post(models.Model):
#     user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
#     title = models.CharField(max_length=255, null=True)  # Added max_length
#     description = models.CharField(max_length=500, null=True)  # Added max_length
#     thumbnail = models.CharField(max_length=255, null=True, blank=True)
#     isPrivate = models.BooleanField(default=False)
#     url = models.CharField(max_length=255, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = "posts"
