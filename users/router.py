from django.conf import settings
# from django.conf.urls import include, url
from django.urls import include, re_path
from rest_framework import routers

from users.views import AuthViewSet

app_name = 'users'
router = routers.SimpleRouter(trailing_slash=False)

router.register(r"auth", AuthViewSet, basename="AuthViewSet")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
