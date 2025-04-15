import json
from django.shortcuts import render
from django.db.models import Count
from parameter.models import Section, Filiere, AcademicYear, Promotion
from student.models import Student
from teachers.models import Teacher
from django.http import JsonResponse
from django.template.loader import render_to_string
from affectation.models import Affectation, TypeProjet


def teacher_page(request):
    current_url = request.resolver_match.view_name
    year = request.GET.get("year")

    if not year:
        academic = AcademicYear.objects.get(is_current=True)
    else:
        academic = AcademicYear.objects.get(year=year)

    filiere_with_student_count = Filiere.objects.filter(
        student_orientation_set__academic_year=academic  # Traversée de relation correcte
    ).annotate(student_count=Count("student_orientation_set", distinct=True))

    # departements = Filiere.objects.filter(section__sigle=sigle)
    sections = Section.objects.all()
    teachers = Teacher.objects.all()
    promotions = Promotion.objects.all()
    students = Student.objects.all()
    academic_years = AcademicYear.objects.filter().order_by("-created_at")

    return render(
        request,
        "pages/teachers/panel.html",
        {
            "filieres": filiere_with_student_count,
            "academics": academic_years,
            "sections": sections,
            "teachers": teachers,
            # "departements": departements,
            "promotions": promotions,
            "students": students,
        },
    )


def get_students_by_teacher(request):
    teacher_id = request.GET.get("teacher_id")

    if not teacher_id:
        return JsonResponse({"affectations": []})

    try:
        teacher = Teacher.objects.get(id=teacher_id)
        academic = AcademicYear.objects.get(is_current=True)
        affectations = (
            Affectation.objects.filter(teacher=teacher, academic_year=academic)
            .select_related("student")
            .values(
                "id",
                "student",
                "promotion__code",  # suppose que promotion est un modèle lié
                "section__sigle",  # suppose que orientation est un modèle lié
               
            )
        )

        return JsonResponse({"affectations": list(affectations)})
    except (Teacher.DoesNotExist, AcademicYear.DoesNotExist):
        return JsonResponse({"affectations": []})
