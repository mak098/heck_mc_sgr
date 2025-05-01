from affectation.models import Affectation
from rest_framework.response import Response
from rest_framework import viewsets, status
import openpyxl
from parameter.models import Section, Promotion, AcademicYear
from teachers.models import Teacher
from django.http import JsonResponse


def import_excel_file(request):

    excel_file = request.FILES.get("file")
    if not excel_file:
        return JsonResponse(
            {"error": "Aucun fichier fourni."}, status=status.HTTP_400_BAD_REQUEST
        )

    # try:
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active
    headers = [cell.value.strip().lower() for cell in sheet[1]]
    success_count = 0
    errors = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        # try:
        teacher = Teacher.objects.get(matricule=row_data["teacher"])
        section = (
            Section.objects.get(id=row_data["section"])
            if row_data.get("section")
            else None
        )
        promotion = (
            Promotion.objects.get(id=row_data["promotion"])
            if row_data.get("promotion")
            else None
        )
        academic_year = AcademicYear.objects.get(year=row_data["academic_year"])
        matricule=row_data.get("matricule", "-")
        if Affectation.objects.filter(teacher=teacher,matricule=matricule,academic_year=academic_year).exists():pass
        Affectation.objects.create(
            teacher=teacher,
            section=section,
            promotion=promotion,
            student=row_data.get("names", "-"),
            matricule=matricule,
            academic_year=academic_year,
            affected_by=request.user,
        )
        success_count += 1

        # except Exception as e:
        #     errors.append({"row": row_data, "error": str(e)})

    return JsonResponse(
        {
            "message": f"{success_count} affectations importées avec succès.",
            "errors": errors,
        },
        status=status.HTTP_200_OK,
    )

    # except Exception as e:
    #     return JsonResponse(
    #         {"error": f"Erreur lors de la lecture du fichier : {str(e)}"},
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )
