import openpyxl
from django.http import HttpResponse
from .models import Student
from parameter.models import AcademicYear

def download_students_excel(request,obj):
    # Créer un fichier Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Liste des étudiants"

    # Définir les en-têtes
    headers = [
        "Matricule",
        "Noms",
        "Lieu de naissance",
        "Sexe",
        "Nationalité",
        "FORMATION ANTERIEURE",
        "Statut",
        "TELEPHONE",
        "Email",
        "Orientation",
        "Promotion",
        "Année academique",
    ]
    sheet.append(headers)
    academic = AcademicYear.objects.get(is_current=True)
    # Ajouter les données des étudiants
    students = Student.objects.filter(academic_year=academic)
    for student in students:
        sheet.append(
            [
                student.matricule,
                student.names,
                student.date_and_place_of_birth,
                student.gender,
                student.nationality,
                student.previous_training,
                student.status,
                student.phone,
                student.email,
                student.orientation.name if student.orientation else "",
                student.promotion.name if student.promotion else "",
                student.academic_year.year if student.academic_year else "",
            ]
        )

    # Préparer la réponse HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="etudiant master complementaire.xlsx"'

    # Sauvegarder le fichier Excel dans la réponse
    workbook.save(response)
    return response
