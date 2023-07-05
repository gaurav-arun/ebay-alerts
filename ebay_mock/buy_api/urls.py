from django.urls import path

from . import views

urlpatterns = [
    path("browse/v1/item_summary/search", views.BuyAPI.as_view(), name="buy_api"),
]
