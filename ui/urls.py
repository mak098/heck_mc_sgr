from django.urls import path
from . import views
from . import rapportPdf
from . import rapportTeacherPdf
from . import orientationFiliere
from . import affectations
from . import teacher
from . import import_affectation
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
    path(
        "affectation-by-section/<str:sigle>",
        affectations.affectation_page,
        name="affectation-by-section",
    ),
    path(
        "importation_page",
        affectations.importation_page,
        name="importation_page",
    ),
    path(
        "importation_payement_page",
        affectations.importation_payement_page,
        name="importation_payement_page",
    ),
    path(
        "importation_update_tuteur_page",
        affectations.importation_update_tuteur_page,
        name="importation_update_tuteur_page",
    ),
    path("get-students/", affectations.get_students, name="get_students"),
    path(
        "get_students_by_teacher/",
        affectations.get_students_by_teacher,
        name="get_students_by_teacher",
    ),
    path(
        "download-teacher-student/<str:year>/<int:teacher>",
        rapportTeacherPdf.ExportPdf.getTeacherStudent,
        name="download-teacher-pdf",
    ),
    path(
        "download-teachers-synthese/<str:year>",
        rapportTeacherPdf.ExportPdf.getTeacherSynthese,
        name="download-teacher-synthese",
    ),
    path(
        "download-teachers-synthese-paiement/<str:year>",
        rapportTeacherPdf.ExportPdf.getAllTeacherPayementSynthese,
        name="getAllTeacherPayementSynthese",
    ),
    path(
        "getAllTeacherStudent/<str:year>",
        rapportTeacherPdf.ExportPdf.getAllTeacherStudent,
        name="getAllTeacherStudent",
    ),
    path("teacher-page/", teacher.teacher_page, name="teacher-page"),
    path(
        "teacher-get-student/",
        teacher.get_students_by_teacher,
        name="teacher-get-student",
    ),
    path(
        "import-excel/",
        import_affectation.import_excel_file,
        name="import_affectation",
    ),
    path(
        "import_payement/",
        import_affectation.import_payement,
        name="import_payement",
    ),
    path(
        "import_update_tuteur/",
        import_affectation.import_update_tuteur,
        name="import_update_tuteur",
    ),
]
