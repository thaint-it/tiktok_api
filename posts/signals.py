 # signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Message,Comment,Like,Favorite
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from users.models.user import Follower


@receiver(post_save, sender=Message)
def message_created_signal(sender, instance, created, **kwargs):
    if created:
        # Logic when a new message is created
        # You can send notifications or trigger a WebSocket event here
         # Get the channel layer
        channel_layer = get_channel_layer()
       
        if channel_layer:
            # Trigger WebSocket event (send to recipient's room group)
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.to_user.id}",  # Send to the recipient's WebSocket group
                {
                    'type': 'send_message',  # This is the name of the method in the consumer
                    'id':instance.id,
                }
            )

@receiver(post_save, sender=Like)
def like_created_signal(sender, instance, created, **kwargs):
    if created:
        # Logic when a new message is created
        # You can send notifications or trigger a WebSocket event here
         # Get the channel layer
        channel_layer = get_channel_layer()
       
        print(f"liked post of user {instance.post.user.id}")
        if channel_layer:
            # Trigger WebSocket event (send to recipient's room group)
            async_to_sync(channel_layer.group_send)(
                f"noti_user_{instance.post.user.id}",  # Send to the recipient's WebSocket group
                {
                    'type': 'send_notify',  # This is the name of the method in the consumer
                    'notify_type':"LIKE",
                    'id':instance.post.user.id,
                }
            )
            

@receiver(post_save, sender=Comment)
def comment_created_signal(sender, instance, created, **kwargs):
    if created:
        # Logic when a new message is created
        # You can send notifications or trigger a WebSocket event here
         # Get the channel layer
        channel_layer = get_channel_layer()
       
        print(f"commented post of user {instance.post.user.id}")
        if channel_layer:
            # Trigger WebSocket event (send to recipient's room group)
            async_to_sync(channel_layer.group_send)(
                f"noti_user_{instance.post.user.id}",  # Send to the recipient's WebSocket group
                {
                    'type': 'send_notify',  # This is the name of the method in the consumer
                    'notify_type':"COMMENT",
                    'id':instance.post.user.id,
                }
            )
            

@receiver(post_save, sender=Favorite)
def favorite_created_signal(sender, instance, created, **kwargs):
    if created:
        # Logic when a new message is created
        # You can send notifications or trigger a WebSocket event here
         # Get the channel layer
        channel_layer = get_channel_layer()
       
        print(f"Favorited post of user {instance.post.user.id}")
        if channel_layer:
            # Trigger WebSocket event (send to recipient's room group)
            async_to_sync(channel_layer.group_send)(
                f"noti_user_{instance.post.user.id}",  # Send to the recipient's WebSocket group
                {
                    'type': 'send_notify',  # This is the name of the method in the consumer
                    'notify_type':"FAVOTITE",
                    'id':instance.post.user.id,
                }
            )

@receiver(post_save, sender=Follower)
def message_created_signal(sender, instance, created, **kwargs):
    if created:
        # Logic when a new message is created
        # You can send notifications or trigger a WebSocket event here
         # Get the channel layer
        channel_layer = get_channel_layer()
       
        print(f"follwed from user {instance.following.id}")
        if channel_layer:
            # Trigger WebSocket event (send to recipient's room group)
            async_to_sync(channel_layer.group_send)(
                f"noti_user_{instance.following.id}",  # Send to the recipient's WebSocket group
                {
                    'type': 'send_notify',  # This is the name of the method in the consumer
                    'notify_type':"FOLLOWED",
                    'id':instance.following.id,
                }
            )

