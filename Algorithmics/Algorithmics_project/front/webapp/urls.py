# myproject/urls.py
from django.urls import path
from pages import views

urlpatterns = [
    path("", views.mapbox_map, name="mapbox_map"),
]