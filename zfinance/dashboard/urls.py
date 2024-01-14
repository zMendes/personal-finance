from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("insert", views.add_movement, name="add movement"),
]
