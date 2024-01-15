from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("movement_by_month_year/<year>/<month>",
         views.get_movement_from_month_year, name='get movement from month'),
    path("insert", views.add_movement, name="add movement"),
]
