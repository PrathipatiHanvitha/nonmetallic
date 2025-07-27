from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("adminlogin", views.adminlogin, name="adminlogin"),
    path("clientsignup", views.clientsignup, name="clientsignup"),
    path("clientsignin", views.clientsignin, name="clientsignin"),
    path("client", views.client, name="client"),
    path("encrypt", views.encrypt_view, name="encrypt"),
    path("decrypt", views.decrypt_view, name="decrypt"),
    path("manage_keys", views.manage_keys, name="manage_keys"),
]