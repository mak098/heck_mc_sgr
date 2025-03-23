import json
from django.shortcuts import render
from django.db.models import Count
from parameter.models import Section,Filiere, AcademicYear, Promotion
from student.models import Student
from django.http import JsonResponse
from django.template.loader import render_to_string

def get_students(request,sigle):
    current_url = request.resolver_match.view_name
    year = request.GET.get("year")

    if not year:
        academic = AcademicYear.objects.get(is_current=True)
    else:
        academic = AcademicYear.objects.get(year=year)

    filiere_with_student_count = Filiere.objects.filter(
        student_orientation_set__academic_year=academic  # Traversée de relation correcte
    ).annotate(student_count=Count("student_orientation_set", distinct=True))

    filieres = Filiere.objects.all()
    academic_years = AcademicYear.objects.filter().order_by("-created_at")
    promotions = Promotion.objects.all()
    filiere = Filiere.objects.get(sigle=sigle)
    academic = AcademicYear.objects.get(is_current=True)
    students = Student.objects.filter(academic_year=academic, orientation=filiere)
    sections = Section.objects.all()
    return render(
        request,
        "pages/studentsfiliere.html",
        {
            "students": students,
            "filiere_list": filieres,
            "filieres": filiere_with_student_count,
            "promotions": promotions,
            "academics": academic_years,
            "sections":sections
        },
    )
