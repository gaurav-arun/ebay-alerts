from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r"alert", views.AlertViewSet, basename="alert")

urlpatterns = [
    path("", include(router.urls)),
]
