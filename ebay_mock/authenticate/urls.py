from django.urls import path

from . import views

urlpatterns = [
    path("v1/oauth2/token/", views.ClientCredentials.as_view(), name="client_credentials"),
]
