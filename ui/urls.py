from django.urls import path
from . import views
from . import rapportPdf
from . import orientationFiliere
urlpatterns = [
    path("", views.index, name="dash"),
    path("tab-dash/", views.get_academic_data, name="tab-dash"),
    path(
        "update-promotion/<int:promotion>",
        views.update_promotion,
        name="update-promotion",
    ),
    path(
        "download-pdf/<str:year>",
        rapportPdf.ExportPdf.get_pdf_for_all_section_in_by_year,
        name="download-pdf",
    ),
    path("login", views.login_page, name="login-page"),
    path("signout", views.logout_view, name="signout"),
    path(
        "students_by_filiere/<str:sigle>",
        orientationFiliere.get_students,
        name="filiere-students",
    ),
]
