from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # homepage
    path("create/", views.create_order, name="create_order"),
    path("success/", views.order_success, name="order_success"),
]
