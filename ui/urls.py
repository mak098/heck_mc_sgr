from django.urls import path
from . import views
from . import orientationFiliere
urlpatterns = [
    path("", views.index, name="dash"),
    path("tab-dash/", views.get_academic_data, name="tab-dash"),
    path("login", views.login_page, name="login-page"),
    path("students_by_filiere/<str:sigle>", orientationFiliere.get_students, name="filiere-students"),
]
