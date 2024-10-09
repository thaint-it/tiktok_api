# your_app_name/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs  # To parse the query string
from channels.db import database_sync_to_async

from utils.logging import CommonLogger

# from users.models.user import User


class NotificationConsumer(AsyncWebsocketConsumer):
    logger = CommonLogger("NotificationConsumer")
    async def connect(self):
        # Get the user ID from the URL path
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = "all_users"  # Common group for all users
        self.user_group_name = f"noti_user_{self.user_id}"  # Common group for all users

        # Join the user's group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        # Set is_online to True
        from users.models import User  # Deferred import

        user = await database_sync_to_async(User.objects.get)(id=self.user_id)
        user.is_online = True
        await database_sync_to_async(user.save)()

        # Accept the WebSocket connection
        await self.accept()
        
        # Send a message to the group about the connection status
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notify",
                "id": self.user_id,
                "notify_type": "CONNECTED"
            }
        )
        

    async def disconnect(self, close_code):
        
         # Set is_online to True
        from users.models import User  # Deferred import
        # Set is_online to False for the user
        user = await database_sync_to_async(User.objects.get)(id=self.user_id)
        user.is_online = False
        await database_sync_to_async(user.save)()

        # Leave the user's group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        
        # Send a message to the group about the disconnection status
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notify",
                "id": self.user_id,
                "notify_type": "DISCONNECTED"
            }
        )
    async def receive(self, text_data):
        # Handle received data from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send a response
        await self.send(text_data=json.dumps({"message": message}))

    # Handler for the 'send_message' event
    async def send_message(self, event):
         # Send the user status update to the WebSocket
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "type": "NEW_MESSAGE"
        }))
        
    # Handler for user status updates
    async def send_notify(self, event):
        self.logger.info(f"Info: {event['notify_type']}")
        # Send the user status update to the WebSocket
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "type": event["notify_type"]
        }))
        
        
class MessageConsumer(AsyncWebsocketConsumer):
    logger = CommonLogger("NotificationConsumer")
    async def connect(self):
        # Get the user ID from the URL path
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"user_{self.user_id}"  # Common group for all users

        # Join the user's group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_send(
             f"user_{self.user_id}",
            {
                "type": "user_status",
                "id": self.user_id,
                "status": "CONNECTED"
            }
        )
        
        # Accept the WebSocket connection
        await self.accept()
        
        # Send a message to the group about the connection status
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "user_status",
                "id": self.user_id,
                "status": "CONNECTED"
            }
        )
        

    async def disconnect(self, close_code):
        # Leave the user's group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        
    # Handler for the 'send_message' event
    async def send_message(self, event):
        self.logger.info(f"Info: NEW_MESSAGE to {event['id']}")
         # Send the user status update to the WebSocket
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "type": "NEW_MESSAGE"
        }))
        
    async def user_status(self, event):
    # Send the user status update to the WebSocket
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "type": event["status"]
        }))
        