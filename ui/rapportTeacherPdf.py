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
from django.db.models import Count
import asyncio


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
    def getTeacherStudent(self, year, teacher):
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

        pdf = CustomPDF(orientation="P")  # Portrait
        pdf.add_page()

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Republique democratique du Congo".upper(), 0, 1, "C")
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 2, "Ministère de l'Enseignement Supérieur et Universitaire".upper(), 0, 1, "C")

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 10, firm.name, 0, 1, "C")

        logo_path = "media/" + str(firm.logo)
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=(pdf.w / 2 - 12.5), y=pdf.get_y(), w=25, h=25)
        else:
            pdf.cell(0, 10, "Logo non trouvé", 0, 1, "C")
        pdf.ln(25)
        pdf.cell(0, 10, firm.service.upper(), 0, 1, "C")

        pdf.ln(1)
        rect_width = pdf.w / 3
        rect_height = 4
        y_position = pdf.get_y()
        pdf.set_fill_color(255, 0, 0)
        pdf.rect(x=0, y=y_position, w=rect_width, h=rect_height, style="FD")
        pdf.set_fill_color(255, 255, 0)
        pdf.rect(x=rect_width, y=y_position, w=rect_width, h=rect_height, style="FD")
        pdf.set_fill_color(0, 0, 255)
        pdf.rect(x=rect_width * 2, y=y_position, w=rect_width, h=rect_height, style="FD")
        pdf.ln(10)

        _teacher = Teacher.objects.get(id=teacher)

        pdf.set_font("Arial", "", 10)
        pdf.cell(30, 4, "Grade :", 0, 0, "L")
        pdf.cell(40, 4, _teacher.grade.grade, 0, 1, "L")
        pdf.ln(3)
        pdf.cell(30, 4, "Matricule :", 0, 0, "L")
        pdf.cell(40, 4, _teacher.matricule, 0, 1, "L")
        pdf.ln(3)
        pdf.cell(30, 4, "Noms :", 0, 0, "L")
        pdf.cell(40, 4, f"{_teacher.first_name} {_teacher.last_name} {_teacher.name}", 0, 1, "L")
        pdf.ln(3)

        affectations = Affectation.objects.filter(academic_year=academic, teacher=teacher)
        summary = affectations.values("section__sigle", "promotion__code").annotate(total=Count("id")).order_by("section__sigle", "promotion__code")
        total_general = affectations.count()

        pdf.set_font("Arial", "B", 9)
        pdf.cell(0, 8, "Récapitulatif par promotion", 0, 1, "L")
        pdf.set_fill_color(200, 200, 200)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(55, 8, "Section", 1, 0, "C", fill=True)
        pdf.cell(45, 8, "Promotion", 1, 0, "C", fill=True)
        pdf.cell(30, 8, "Nb Étudiants", 1, 1, "C", fill=True)

        pdf.set_fill_color(255, 255, 255)
        for item in summary:
            section_sigle = item["section__sigle"] or "N/A"
            promotion_code = item["promotion__code"] or "N/A"
            pdf.cell(55, 8, section_sigle, 1, 0, "L")
            pdf.cell(45, 8, promotion_code, 1, 0, "L")
            pdf.cell(30, 8, str(item["total"]), 1, 1, "L")

        pdf.set_fill_color(220, 220, 220)
        pdf.cell(100, 8, "TOTAL GENERAL", 1, 0, "R", fill=True)
        pdf.cell(30, 8, str(total_general), 1, 1, "R", fill=True)
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Etudiants", 0, 1)

        pdf.set_fill_color(0, 0, 0)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 9)
        pdf.cell(15, 8, "Num", 1, 0, "C", fill=True)
        pdf.cell(60, 8, "Noms", 1, 0, "C", fill=True)
        pdf.cell(30, 8, "Section", 1, 0, "C", fill=True)
        pdf.cell(30, 8, "Promotion", 1, 0, "C", fill=True)
        pdf.cell(30, 8, "Payement", 1, 0, "C", fill=True)
        pdf.cell(30, 8, "Percu", 1, 1, "C", fill=True)

        i = 0
        total_management_fees = 0.0
        total_teacher_collected = 0.0
        pdf.set_text_color(0, 0, 0)

        for aff in affectations:
            i += 1
            m_fees = float(aff.management_fees) if aff.management_fees else 0.0
            t_collected = float(aff.teacher_amount_collected) if aff.teacher_amount_collected else 0.0
            total_management_fees += m_fees
            total_teacher_collected += t_collected

            pdf.cell(15, 8, str(i), 1, 0, "L")
            pdf.cell(60, 8, aff.student, 1, 0, "L")
            pdf.cell(30, 8, aff.section.sigle, 1, 0, "L")
            pdf.cell(30, 8, aff.promotion.code if aff.promotion else "N/A", 1, 0, "L")
            pdf.cell(30, 8, f"{m_fees:.2f}", 1, 0, "R")
            pdf.cell(30, 8, f"{t_collected:.2f}", 1, 1, "R")

        # Ligne des totaux
        pdf.set_font("Arial", "B", 9)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(135, 8, "TOTAL", 1, 0, "R", fill=True)
        pdf.cell(30, 8, f"{total_management_fees:.2f}", 1, 0, "R", fill=True)
        pdf.cell(30, 8, f"{total_teacher_collected:.2f}", 1, 1, "R", fill=True)

        # Ligne du disponible
        disponible = total_management_fees - total_teacher_collected
        pdf.set_fill_color(200, 255, 200)
        pdf.set_text_color(0, 100, 0)
        pdf.set_font("Arial", "B", 9)
        pdf.cell(135, 8, "DISPONIBLE", 1, 0, "R", fill=True)
        pdf.cell(60, 8, f"{disponible:.2f}", 1, 1, "R", fill=True)

        # Générer le PDF
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer, dest="S")
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{_teacher.first_name}.pdf"'
        return response

    # returner le rapport pour chaque prof
    def getTeacherSynthese(self,year):
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
        teachers = Teacher.objects.all()

        for teacher in teachers:

            # ========== NOUVEAU TABLEAU RECAPITULATIF ==========
            # Récupérer les données récapitulatives
            affectations = Affectation.objects.filter(
                academic_year=academic, teacher=teacher
            )
            summary = (
                affectations.values(
                    "section__sigle",
                    "promotion__code",
                )
                .annotate(total=Count("id"))
                .order_by(
                    "section__sigle",
                  
                    "promotion__code",
                )
            )

            # Calculer le total général
            total_general = affectations.count()

            # En-tête du tableau récapitulatif
            pdf.set_font("Arial", "B", 9)
            pdf.cell(
                0,
                8,
                f"{teacher.matricule or ''} {getattr(teacher, 'grade', '') or ''}. {teacher.first_name or ''} {teacher.last_name or ''} {teacher.name or ''}",
                0,
                1,
                "L",
            )

            pdf.set_fill_color(200, 200, 200)  # Gris clair
            pdf.set_text_color(0, 0, 0)
            pdf.cell(55, 8, "Section", 1, 0, "C", fill=True)
            pdf.cell(45, 8, "Promotion", 1, 0, "C", fill=True)
            pdf.cell(30, 8, "Nb Étudiants", 1, 1, "C", fill=True)

            # Données du récapitulatif
            pdf.set_fill_color(255, 255, 255)
            for item in summary:
                pdf.cell(55, 8, str(item.get("section__sigle") or ""), 1, 0, "L")
                pdf.cell(45, 8, str(item.get("promotion__code") or ""), 1, 0, "L")
                pdf.cell(30, 8, str(item.get("total") or ""), 1, 1, "R")
            # Ligne du total général
            pdf.set_fill_color(220, 220, 220)  # Gris un peu plus foncé
            pdf.cell(100, 8, "TOTAL GENERAL", 1, 0, "R", fill=True)
            pdf.cell(30, 8, str(total_general), 1, 1, "R", fill=True)

            pdf.ln(5)  

        pdf.set_font("Arial", "B", 10)
        pdf.cell(
            0,
            10,
            f"Secrétaire Général",
            0,
            1,
            "L",
        )
        pdf.ln(5)
        # Sauvegarder le PDF dans un fichier temporaire
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer, dest="S")
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{academic.year}.pdf"'
        )
        return response

    def getAllTeacherStudent(self, year):
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

        pdf = CustomPDF(orientation="P")
        pdf.add_page()

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Republique democratique du Congo".upper(), 0, 1, "C")
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 2, "Ministère de l'Enseignement Supérieur et Universitaire".upper(), 0, 1, "C")

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 10, firm.name, 0, 1, "C")

        logo_path = "media/" + str(firm.logo)
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=(pdf.w / 2 - 12.5), y=pdf.get_y(), w=25, h=25)
        else:
            pdf.cell(0, 10, "Logo non trouvé", 0, 1, "C")
        pdf.ln(25)
        pdf.cell(0, 10, firm.service.upper(), 0, 1, "C")

        pdf.ln(1)
        rect_width = pdf.w / 3
        rect_height = 4
        y_position = pdf.get_y()
        pdf.set_fill_color(255, 0, 0)
        pdf.rect(x=0, y=y_position, w=rect_width, h=rect_height, style="FD")
        pdf.set_fill_color(255, 255, 0)
        pdf.rect(x=rect_width, y=y_position, w=rect_width, h=rect_height, style="FD")
        pdf.set_fill_color(0, 0, 255)
        pdf.rect(x=rect_width * 2, y=y_position, w=rect_width, h=rect_height, style="FD")
        pdf.ln(10)

        teachers = Teacher.objects.all()
        for _teacher in teachers:
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, f"Enseignant : {(_teacher.first_name or '')} {(_teacher.last_name or '')} {(_teacher.name or '')}", 0, 1, "L")
            pdf.set_font("Arial", "", 10)
            pdf.cell(30, 4, "Grade :", 0, 0, "L")
            pdf.cell(40, 4, str(getattr(_teacher.grade, 'grade', '')), 0, 1, "L")
            pdf.ln(3)
            pdf.cell(30, 4, "Matricule :", 0, 0, "L")
            pdf.cell(40, 4, str(_teacher.matricule or ""), 0, 1, "L")
            pdf.ln(3)

            affectations = Affectation.objects.filter(academic_year=academic, teacher=_teacher)
            if not affectations.exists():
                pdf.cell(0, 8, "Aucune affectation pour cet enseignant.", 0, 1, "L")
                pdf.ln(5)
                continue

            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, f"Etudiants", 0, 1)

            pdf.set_fill_color(0, 0, 0)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 9)
            pdf.cell(15, 8, "Num", 1, 0, "C", fill=True)
            pdf.cell(60, 8, "Noms", 1, 0, "C", fill=True)
            pdf.cell(30, 8, "Section", 1, 0, "C", fill=True)
            pdf.cell(30, 8, "Promotion", 1, 0, "C", fill=True)
            pdf.cell(30, 8, "Payement", 1, 0, "C", fill=True)
            pdf.cell(30, 8, "Percu", 1, 1, "C", fill=True)

            i = 0
            total_management_fees = 0.0
            total_teacher_collected = 0.0
            pdf.set_text_color(0, 0, 0)

            for aff in affectations:
                i += 1
                m_fees = float(aff.management_fees) if aff.management_fees else 0.0
                t_collected = float(aff.teacher_amount_collected) if aff.teacher_amount_collected else 0.0
                total_management_fees += m_fees
                total_teacher_collected += t_collected

                pdf.cell(15, 8, str(i), 1, 0, "L")
                pdf.cell(60, 8, remove_non_ascii(aff.student), 1, 0, "L")
                pdf.cell(30, 8, remove_non_ascii(getattr(aff.section, 'sigle', '')), 1, 0, "L")
                pdf.cell(30, 8, remove_non_ascii(getattr(aff.promotion, 'code', 'N/A')), 1, 0, "L")
                pdf.cell(30, 8, f"{m_fees:.2f}", 1, 0, "R")
                pdf.cell(30, 8, f"{t_collected:.2f}", 1, 1, "R")
            # Ligne des totaux
            pdf.set_font("Arial", "B", 9)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(135, 8, "TOTAL", 1, 0, "R", fill=True)
            pdf.cell(30, 8, f"{total_management_fees:.2f}", 1, 0, "R", fill=True)
            pdf.cell(30, 8, f"{total_teacher_collected:.2f}", 1, 1, "R", fill=True)

            # Ligne du disponible
            disponible = total_management_fees - total_teacher_collected
            pdf.set_fill_color(200, 255, 200)
            pdf.set_text_color(0, 100, 0)
            pdf.set_font("Arial", "B", 9)
            pdf.cell(135, 8, "DISPONIBLE", 1, 0, "R", fill=True)
            pdf.cell(60, 8, f"{disponible:.2f}", 1, 1, "R", fill=True)
            pdf.ln(10)

        # Générer le PDF
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer, dest="S")
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="all_teachers_{academic.year}.pdf"'
        return response

import unicodedata


def remove_non_ascii(text):
    if not text:
        return ""
    # Remplace les apostrophes typographiques par des simples
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # Enlève les caractères non-ASCII
    return (
        unicodedata.normalize("NFKD", str(text))
        .encode("ascii", "ignore")
        .decode("ascii")
    )
