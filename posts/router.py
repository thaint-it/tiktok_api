from django.conf import settings
# from django.conf.urls import include, url
from django.urls import include, re_path
from rest_framework import routers

from posts.views import PostViewSet,MessageViewSet

app_name = 'posts'
router = routers.SimpleRouter(trailing_slash=False)

router.register(r"message", MessageViewSet, basename="MessageViewSet")
router.register(r"post", PostViewSet, basename="PostViewSet")


urlpatterns = [
    re_path(r"^", include(router.urls)),
]
