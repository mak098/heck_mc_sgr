from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dash"),
    path("tab-dash/", views.get_academic_data, name="tab-dash"),
]
