from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from django.http import HttpResponse
import datetime
from .models import Section, AcademicYear
from teachers.models import Teacher
from affectation.models import Affectation

def getAllTeacherStudentBySectionExcel(self, sections):
    academic = AcademicYear.objects.get(is_current=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Enseignants par section"

    # En-tête du fichier
    ws.merge_cells("A1:F1")
    ws["A1"] = "RDC - Ministère de l'Enseignement Supérieur et Universitaire"
    ws["A1"].font = Font(bold=True)
    ws["A1"].alignment = Alignment(horizontal="center")

    ws.append([])  # Ligne vide

    # En-têtes du tableau
    headers = [
        "Section",
        "Enseignant",
        "Grade",
        "Matricule Enseignant",
        "Promotion",
        "Nom Etudiant",
        "Matricule Etudiant",
    ]
    ws.append(headers)
    for cell in ws[3]:
        cell.font = Font(bold=True)

    for sec in sections:
        section = Section.objects.get(id=sec["id"])
        teachers = Teacher.objects.all().order_by("-grade__grade")
        for teacher in teachers:
            affectations = Affectation.objects.filter(
                academic_year=academic, teacher=teacher, section=section
            )
            if not affectations.exists():
                continue
            for aff in affectations:
                ws.append(
                    [
                        section.name,
                        f"{teacher.first_name or ''} {teacher.last_name or ''} {teacher.name or ''}".strip(),
                        str(getattr(teacher.grade, "grade", "")),
                        teacher.matricule or "",
                        getattr(aff.promotion, "code", ""),
                        aff.student,
                        aff.matricule,  # Si tu veux le nombre d'étudiants, adapte ici selon ta logique
                    ]
                )

    # Préparer la réponse HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    filename = f"enseignants_par_section_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
