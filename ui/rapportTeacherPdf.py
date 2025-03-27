from django.http import HttpResponse
from fpdf import FPDF
from io import BytesIO
import os
from django.db.models import Sum, F, FloatField
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Prefetch
from rest_framework import viewsets
from datetime import datetime
from parameter.models import AcademicYear, Filiere, Promotion, Firm
from student.models import Student
from teachers.models import Teacher
from affectation.models import Affectation


class CustomPDF(FPDF):
    def footer(self):
        # Position à 1.5 cm du bas
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        current_time = datetime.now()
        self.cell(0, 10, f"{current_time}", 0, 0, "R")
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        # Numéro de page centré

        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

class ExportPdf(viewsets.ModelViewSet):
    def getTeacherStudent(self,year,teacher):
        try:
            if year == "current":
                academic = AcademicYear.objects.get(is_current=True)
            else:
                academic = AcademicYear.objects.get(year=year)
        except AcademicYear.DoesNotExist:
            return HttpResponse("Année académique non trouvée", status=404)

        firm = Firm.objects.all().first()
        if not firm:
            return HttpResponse("Aucune entreprise trouvée", status=404)

        pdf = CustomPDF(orientation="P")  # Mode paysage
        pdf.add_page()

        # Titre principal
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Republique democratique du Congo".upper(), 0, 1, "C")

        # Sous-titre
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(
            0,
            2,
            "Ministère de l'Enseignement Supérieur et Universitaire".upper(),
            0,
            1,
            "C",
        )

        # Nom de l'entreprise
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 10, firm.name, 0, 1, "C")
        pdf.cell(0, 10, firm.service, 0, 1, "C")

        # Logo sous le nom de l'entreprise avec un interligne de 10
        pdf.ln(1)  # Interligne de 10
        logo_path = "media/" + str(firm.logo)
        if os.path.exists(logo_path):
            pdf.image(
                logo_path,
                x=(pdf.w / 2 - 12.5),
                y=pdf.get_y(),
                w=25,
                h=25,
                type="",
                link="",
            )  # Centrer le logo
        else:
            pdf.cell(0, 10, "Logo non trouvé", 0, 1, "C")

        # Trois barres sous le logo avec un interligne de 10
        pdf.ln(28)  # Interligne de 10
        rect_width = (
            pdf.w / 3
        )  # Largeur de chaque rectangle (1/3 de la largeur de la page)
        rect_height = 4  # Hauteur des rectangles
        y_position = pdf.get_y()  # Position Y après le logo et l'interligne

        # Rectangle rouge
        pdf.set_fill_color(255, 0, 0)
        pdf.rect(x=0, y=y_position, w=rect_width, h=rect_height, style="FD")

        # Rectangle jaune
        pdf.set_fill_color(255, 255, 0)
        pdf.rect(x=rect_width, y=y_position, w=rect_width, h=rect_height, style="FD")

        # Rectangle bleu
        pdf.set_fill_color(0, 0, 255)
        pdf.rect(
            x=rect_width * 2, y=y_position, w=rect_width, h=rect_height, style="FD"
        )
        pdf.ln(10)
        _teacher = Teacher.objects.get(id=teacher)

        pdf.set_font("Arial", "", 10)
        pdf.cell(30, 4, "Titre :", 0, 0, "L")
        pdf.cell(40, 4, _teacher.grade.grade, 0, 1, "L")
        pdf.ln(3)
        pdf.cell(30, 4, "Matricule :", 0, 0, "L")
        pdf.cell(40, 4, _teacher.matricule, 0, 1, "L")
        pdf.ln(3)

        # Noms
        pdf.cell(30, 4, "Noms :", 0, 0, "L")
        pdf.cell(
            40,
            4,
            f"{_teacher.first_name} {_teacher.last_name} {_teacher.name}",
            0,
            1,
            "L",
        )
        pdf.ln(3)

        # En-tête du tableau avec fond noir
        pdf.set_fill_color(0, 0, 0)  # Noir
        pdf.set_text_color(255, 255, 255)  # Blanc
        pdf.set_font("Arial", "B", 9)
        pdf.cell(
            20, 8, "Matricule", 1, 0, "L", fill=True
        )  # Largeur ajustée
        pdf.cell(75, 8, "Noms", 1, 0, "L", fill=True)  # Largeur ajustée
        pdf.cell(20, 8, "section", 1, 0, "L", fill=True)  # Largeur ajustée
        pdf.cell(
            40, 8, "Depart.", 1, 0, "L", fill=True
        )  # Largeur ajustée
        pdf.cell(35, 8, "Prom.", 1, 1, "L", fill=True)  # Largeur ajustée

        # Liste des étudiants
        pdf.set_fill_color(255, 255, 255)  # Fond blanc
        pdf.set_text_color(0, 0, 0) 

        affectations = Affectation.objects.filter(academic_year=academic,teacher=teacher)
        for affection in affectations:
            pdf.cell(20, 8, affection.student.matricule, 1, 0, "L")
            pdf.cell(75, 8, affection.student.names, 1, 0, "L")
            pdf.cell(20, 8, affection.student.orientation.section.sigle, 1, 0, "L")
            pdf.cell(40, 8, affection.student.orientation.sigle, 1, 0, "L")
            pdf.cell(
                35, 8, affection.student.promotion.code, 1, 1, "L"
            )
        # pdf.ln(5)
        pdf.ln(9)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(
            0,
            10,
            f"Secrétaire Général",
            0,
            1,
            "L",
        )

        # Sauvegarder le PDF dans un fichier temporaire
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer, dest="S")
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{_teacher.first_name}.pdf"'
        return response
