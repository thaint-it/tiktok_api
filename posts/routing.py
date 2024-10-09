from django.urls import path
from . import consumers

websocket_urlpatterns = [
   path('ws/notification/<int:user_id>/', consumers.NotificationConsumer.as_asgi()),  # Ensure this path matches
   path('ws/messages/<int:user_id>/', consumers.MessageConsumer.as_asgi()),  # Ensure this path matches
]
