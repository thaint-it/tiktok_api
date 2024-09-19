# from django.conf.urls import include, url
from django.urls import include, re_path
from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^api/", include("users.router", namespace="v1")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += (re_path(r"^favicon\.ico$", RedirectView.as_view(url="/docs/img/favicon.ico")),)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)