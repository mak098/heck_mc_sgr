import json
from django.shortcuts import render
from django.db.models import Count
from parameter.models import Section,Filiere, AcademicYear, Promotion
from student.models import Student
from teachers.models import Teacher
from django.http import JsonResponse
from django.template.loader import render_to_string
from affectation.models import Affectation,TypeProjet

def affectation_page(request, sigle):
    current_url = request.resolver_match.view_name
    year = request.GET.get("year")

    if not year:
        academic = AcademicYear.objects.get(is_current=True)
    else:
        academic = AcademicYear.objects.get(year=year)

    filiere_with_student_count = Filiere.objects.filter(
        student_orientation_set__academic_year=academic  # Traversée de relation correcte
    ).annotate(student_count=Count("student_orientation_set", distinct=True))

    departements = Filiere.objects.filter(section__sigle=sigle)
    sections = Section.objects.all()
    teachers = Teacher.objects.all()
    promotions = Promotion.objects.all()
    students = Student.objects.all()
    academic_years = AcademicYear.objects.filter().order_by("-created_at")

    return render(
        request,
        "pages/affectations/aff-main-panel.html",
        {
            "filieres": filiere_with_student_count,
            "academics": academic_years,
            "sections": sections,
            "teachers": teachers,
            "departements": departements,
            "promotions": promotions,
            "students": students,
        },
    )
def importation_page(request):
    current_url = request.resolver_match.view_name
    year = request.GET.get("year")

    if not year:
        academic = AcademicYear.objects.get(is_current=True)
    else:
        academic = AcademicYear.objects.get(year=year)

    filiere_with_student_count = Filiere.objects.filter(
        student_orientation_set__academic_year=academic  # Traversée de relation correcte
    ).annotate(student_count=Count("student_orientation_set", distinct=True))

    sections = Section.objects.all()
    teachers = Teacher.objects.all()
    promotions = Promotion.objects.all()
    students = Student.objects.all()
    academic_years = AcademicYear.objects.filter().order_by("-created_at")

    return render(
        request,
        "pages/affectations/import_excel.html",
        {
            "filieres": filiere_with_student_count,
            "academics": academic_years,
            "sections": sections,
            "teachers": teachers,
            "promotions": promotions,
            "students": students,
        },
    )


def get_students(request):
    departement_id = request.GET.get("departement_id")
    promotion_id = request.GET.get("promotion_id")
    academic = AcademicYear.objects.get(is_current=True)
    depart = Filiere.objects.get(id = departement_id)
    prom = Promotion.objects.get(id=promotion_id)
    students = Student.objects.filter(
        orientation=depart, promotion=prom, academic_year=academic
    ).values("id", "matricule", "names")

    return JsonResponse({"students": list(students)})


def get_students_by_teacher(request):
    teacher_id = request.GET.get("teacher_id")

    teacher = Teacher.objects.get(id=teacher_id)
    academic = AcademicYear.objects.get(is_current=True)
    affectations = Affectation.objects.filter(
        teacher=teacher, academic_year=academic
    ).values(
        "id",
        "student",
        "matricule",
        "type",
        "management_fees",
        "teacher_amount_collected",
    )
    if teacher_id:       
        return JsonResponse({"affectations": list(affectations)})

    return JsonResponse({"affectations": []})

def add_affectation(request):
    teacher_id = request.GET.get("teacher_id")
    type_id = request.GET.get("type_id")
    student_id = request.GET.get("student_id")
    academic = AcademicYear.objects.get(is_current=True)
    subject = request.GET.get("subject")
    teacher = Teacher.objects.get(id=teacher_id)
    type = TypeProjet.objects.get(id =type_id)
    student = Student.objects.get(id=student_id)

    aff = Affectation.objects.create(
        type=type,
        teacher=teacher,
        subject=subject,
        student=student,
        academic_year=academic,
        affected_by=request.user,
    )
    if aff :
        return JsonResponse({"affectations": list(aff)})
    return JsonResponse({"message":"Echec"})

def update_affectation(request):

    affectation_id = request.GET.get("affectation_id")
    teacher_id = request.GET.get("teacher_id")
    type_id = request.GET.get("type_id")
    student_id = request.GET.get("student_id")
    academic = AcademicYear.objects.get(is_current=True)
    subject = request.GET.get("subject")
    teacher = Teacher.objects.get(id=teacher_id)
    type = TypeProjet.objects.get(id =type_id)
    student = Student.objects.get(id=student_id)
    aff = Affectation.objects.get(id=affectation_id)
    aff.type = type
    aff.academic_year = academic
    aff.teacher = teacher
    aff.student = student
    aff.subject = subject
    aff.save()
    if aff :
        return JsonResponse({"affectations": list(aff)})
    return JsonResponse({"message":"Echec"})

def teacher_affections(request):
    academic_id =request.GET.get("academic_id")
    teacher_id =request.GET.get("teacher_id")
    academic_year = AcademicYear.objects.get(is_current=True)

    if  academic_id:
        academic_year = AcademicYear.objects.get(id=academic_id)
