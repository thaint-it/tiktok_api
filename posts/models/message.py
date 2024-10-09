from django.db import models
from django.forms import ValidationError
from posts.models.post import Post
from users.models import User
from base_services.models  import AutoTimeStampedModel

# Create your models here.
class Message(AutoTimeStampedModel):
    from_user = models.ForeignKey(User, null=True,related_name='sent_messages', on_delete=models.DO_NOTHING)
    to_user = models.ForeignKey(User, null=True,related_name='received_messages', on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=500, null=True)  # Added max_length
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    is_read=models.BooleanField(null=True,default=False)
    class Meta:
        db_table = "messages"
        
    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("Sender and recipient cannot be the same.")
        if not self.content:
            raise ValidationError("Content cannot be empty.")
