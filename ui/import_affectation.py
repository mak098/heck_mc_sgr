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
        print(
            f">>>>>>>>>>>>>>>>>>>>>>>>teacher {row_data["teacher"]} student{row_data.get("names", "-")}",
        )
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
        if not Affectation.objects.filter(teacher=teacher,matricule=matricule,academic_year=academic_year).exists():
            if not Affectation.objects.filter(matricule=matricule,academic_year=academic_year).exists():
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

def import_payement(request):

    excel_file = request.FILES.get("file")
    if not excel_file:
        return JsonResponse(
            {"error": "Aucun fichier fourni."}, status=status.HTTP_400_BAD_REQUEST
        )

    # try:
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active
    headers = [
        (cell.value.strip().lower() if cell.value is not None else "")
        for cell in sheet[1]
    ]
    success_count = 0
    errors = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))

        academic_year = AcademicYear.objects.get(year=row_data["academic_year"])
        matricule=row_data.get("matricule", "-")
        if Affectation.objects.filter(matricule=matricule,academic_year=academic_year).exists():
            affectation = Affectation.objects.filter(matricule=matricule,academic_year=academic_year).first()

            affectation.management_fees = row_data.get("management_fees", 0.00)
            affectation.save()
            success_count += 1

    return JsonResponse(
        {
            "message": f"{success_count} affectations importées avec succès.",
            "errors": errors,
        },
        status=status.HTTP_200_OK,
    )


def import_update_tuteur(request):
    excel_file = request.FILES.get("file")
    if not excel_file:
        return JsonResponse(
            {"error": "Aucun fichier fourni."}, status=status.HTTP_400_BAD_REQUEST
        )

    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active
    headers = [
        (cell.value.strip().lower() if cell.value is not None else "")
        for cell in sheet[1]
    ]
    success_count = 0
    errors = []

    for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        try:
            row_data = dict(zip(headers, row))
            academic_year = AcademicYear.objects.get(is_current=True)
            matricule = row_data.get("matricule etudiant", "-")
            old_teacher_matricule = row_data.get("matricule enseignant", "-")
            old_teacher = Teacher.objects.filter(
                matricule=old_teacher_matricule
            ).first()
            new_teacher_matricule = row_data.get("matricule enseignant", "-")
            new_teacher = Teacher.objects.filter(
                matricule=new_teacher_matricule
            ).first()

            if not old_teacher or not new_teacher:
                raise ValueError("Enseignant introuvable")

            affectation = Affectation.objects.filter(
                matricule=matricule, teacher=old_teacher, academic_year=academic_year
            ).first()
            if not affectation:
                raise ValueError("Affectation introuvable")

            affectation.teacher = new_teacher
            affectation.save()
            success_count += 1
        except Exception as e:
            errors.append(f"Ligne {idx}: {str(e)}")

    return JsonResponse(
        {
            "message": f"{success_count} affectations modifiées avec succès.",
            "errors": errors,
        },
        status=status.HTTP_200_OK,
    )
