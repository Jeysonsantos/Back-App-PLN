from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main.views import create

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('texto/', create),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
