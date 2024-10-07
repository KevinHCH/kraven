from django.urls import path

# from the package web import views
from web import views

urlpatterns = [
    path("", views.index, name="index"),
]
