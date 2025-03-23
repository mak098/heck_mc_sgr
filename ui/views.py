import json
from django.shortcuts import render
from django.db.models import Count
from parameter.models import Section,Filiere,AcademicYear,Promotion
from authentication.models import User
from student.models import Student
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404
from .forms import SigninForm
from rest_framework.response import Response
from rest_framework import viewsets,status
from django.conf import settings
from django.conf.urls import handler404
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, "pages/404.html", status=404)


if settings.DEBUG is False:
    handler404 = custom_404

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
    sections = Section.objects.all()

    promotions = (
        Promotion.objects.filter(student_promotion_set__academic_year=academic)
        .annotate(student_count=Count("student_promotion_set"))
        .values("id","code" ,"name", "student_count")
    )
    promotion_data = list(promotions)

    return render(
        request,
        "pages/dash.html",
        {
            "filiere_list": filieres,
            "sections": sections,
            "filieres": filiere_with_student_count,
            "students": total_students,
            "academics": academic_years,
            "feminin": feminin,
            "masculin": masculin,
            "promotions": promotion_data,
        },
    )

def login_page(request):
    error = False
    if request.user.is_authenticated:
        return redirect('dash')
    else:
        form = SigninForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dash')
            else:
                error = True
    return render(request, "pages/login.html", locals())


@login_required
def logout_view(request):
    logout(request)
    return redirect("dash")


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
    promotions = (
        Promotion.objects.filter(student_promotion_set__academic_year=academic)
        .annotate(student_count=Count("student_promotion_set"))
        .values("id", "code", "name", "student_count")
    )
    promotion_data = list(promotions)

    # Retourner les données sous forme de JSON
    data = {
        "html": render_to_string(
            "dash-cards/filieres-count-students.html",
            {
                "filiere_list": filieres,
                "filieres": filiere_with_student_count,
                "students": total_students,
                "academics": academic_years,
                "feminin": feminin,
                "masculin": masculin,
                "promotions": promotion_data,
            },
        )
    }
    return JsonResponse(data)

def update_promotion(request,promotion):
    pro = Promotion.objects.get(id=promotion)
    students = Student.objects.all()
    for student in students :
        student.promotion =pro
        student.save()
    
    return Response({"message":"update success"},status=status.HTTP_200_OK)
