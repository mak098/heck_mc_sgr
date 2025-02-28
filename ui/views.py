import json
from django.shortcuts import render
from django.db.models import Count
from parameter.models import Filiere,AcademicYear
from student.models import Student
from django.http import JsonResponse
from django.template.loader import render_to_string


def index(request):
    current_url = request.resolver_match.view_name
    year = request.GET.get("year")

    if not year:
        academic = AcademicYear.objects.get(is_current=True)
    else:
        academic = AcademicYear.objects.get(year=year)

    filiere_with_student_count = Filiere.objects.filter(
        student_orientation_set__academic_year=academic  # Traversée de relation correcte
    ).annotate(student_count=Count("student_orientation_set", distinct=True))

    academic_years = AcademicYear.objects.filter().order_by("-created_at")
    # Calcul du nombre total d'étudiants
    total_students = Student.objects.filter(academic_year=academic).count()
    feminin = Student.objects.filter(gender="Féminin", academic_year=academic).count()
    masculin = Student.objects.filter(gender="Masculin", academic_year=academic).count()
    # Ajouter le pourcentage directement dans le queryset
    for filiere in filiere_with_student_count:
        filiere.percentage = (
            (filiere.student_count / total_students * 100) if total_students > 0 else 0
        )

    filieres = Filiere.objects.all()
    labels = []
    masculin_data = []
    feminin_data = []

    for filiere in filieres:
        labels.append(filiere.name)
        masculin_count = Student.objects.filter(
            orientation=filiere, gender="Masculin"
        ).count()
        feminin_count = Student.objects.filter(
            orientation=filiere, gender="Féminin"
        ).count()

        masculin_data.append(masculin_count)
        feminin_data.append(feminin_count)

    return render(
        request,
        "index.html",
        {
            "filieres": filiere_with_student_count,
            "students": total_students,
            "academics": academic_years,
            "feminin": feminin,
            "masculin": masculin,
            "labels": json.dumps(labels),  # ✅ Encodage JSON correct
            "masculin_data": json.dumps(masculin_data),  # ✅
            "feminin_data": json.dumps(feminin_data),  # ✅
            "students": total_students,
        },
    )


def get_academic_data(request):
    year = request.GET.get("year")

    if not year:
        academic = AcademicYear.objects.get(is_current=True)
    else:
        academic = AcademicYear.objects.get(year=year)

    filiere_with_student_count = Filiere.objects.filter(
        student_orientation_set__academic_year=academic  # Traversée de relation correcte
    ).annotate(student_count=Count("student_orientation_set", distinct=True))

    academic_years = AcademicYear.objects.filter().order_by("-created_at")
    # Calcul du nombre total d'étudiants
    total_students = Student.objects.filter(academic_year=academic).count()
    feminin = Student.objects.filter(gender="Féminin", academic_year=academic).count()
    masculin = Student.objects.filter(gender="Masculin", academic_year=academic).count()
    # Ajouter le pourcentage directement dans le queryset
    for filiere in filiere_with_student_count:
        filiere.percentage = (
            (filiere.student_count / total_students * 100) if total_students > 0 else 0
        )

    filieres = Filiere.objects.all()
    labels = []
    masculin_data = []
    feminin_data = []

    for filiere in filieres:
        labels.append(filiere.name)
        masculin_count = Student.objects.filter(
            orientation=filiere, gender="Masculin"
        ).count()
        feminin_count = Student.objects.filter(
            orientation=filiere, gender="Féminin"
        ).count()

        masculin_data.append(masculin_count)
        feminin_data.append(feminin_count)

    # Retourner les données sous forme de JSON
    data = {
        "html": render_to_string(
            "dash-cards/filieres-count-students.html",
            {
                "filieres": filiere_with_student_count,
                "students": total_students,
                "academics": academic_years,
                "feminin": feminin,
                "masculin": masculin,
                "labels": json.dumps(labels),  # ✅ Encodage JSON correct
                "masculin_data": json.dumps(masculin_data),  # ✅
                "feminin_data": json.dumps(feminin_data),  # ✅
                "students": total_students,
            },
        )
    }
    return JsonResponse(data)
