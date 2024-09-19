from rest_framework import viewsets

from base_services.throttles.base import BaseUserThrottle


class GenericViewMixin(viewsets.ViewSet):
    service_class = None
    lookup_field = "pk"
    lookup_url_kwarg = None
    throttle_classes = (BaseUserThrottle,)

