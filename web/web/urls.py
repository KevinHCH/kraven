from django.urls import path

# from the package web import views
from web import views

urlpatterns = [
    path("", views.index, name="index"),
    path("stream", views.stream, name="stream"),
    path("json", views.json_test, name="json"),
]
handler404 = 'core.views.not_found_view'
