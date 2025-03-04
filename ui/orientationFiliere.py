import json
from django.shortcuts import render
from django.db.models import Count
from parameter.models import Filiere, AcademicYear, Promotion
from student.models import Student
from django.http import JsonResponse
from django.template.loader import render_to_string

def get_students(request,sigle):
    current_url = request.resolver_match.view_name
    # year = request.GET.get("year")
    # filiere = request.get("filiere")
    filieres = Filiere.objects.all()
    academic_years = AcademicYear.objects.filter().order_by("-created_at")
    promotions = Promotion.objects.all()
    filiere = Filiere.objects.get(sigle=sigle)
    academic = AcademicYear.objects.get(is_current=True)
    students = Student.objects.filter(academic_year=academic, orientation=filiere)

    return render(
        request,
        "pages/studentsfiliere.html",
        {
            "students": students,
            "filieres":filieres,
            "promotions":promotions,
            "academics":academic_years
        },
    )
