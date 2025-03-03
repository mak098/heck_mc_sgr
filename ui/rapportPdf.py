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
from parameter.models import AcademicYear,Filiere,Promotion,Firm
from student.models import Student
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
    def get_pdf_for_all_section_in_by_year(self, year):
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

        pdf = CustomPDF(orientation="L")  # Mode paysage
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

        # Titre "ETUDIANT FINALISTE"
        pdf.ln(10)  # Interligne de 10 après les barres
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 10, f"ETUDIANT FINALISTE  ({academic.year})", 0, 1, "C")

        # Contenu du tableau
        filieres = Filiere.objects.all()
        for filiere in filieres:
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 10, f"{filiere.name.upper()}", 0, 1)
            pdf.set_text_color(0, 0, 0)

            promotions = Promotion.objects.all()
            for promotion in promotions:
                students = Student.objects.filter(
                    orientation=filiere, promotion=promotion, academic_year=academic
                ).order_by("-matricule")

                if students.exists():
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 8, f"Promotion : {promotion.name}", 0, 1)

                    # En-tête du tableau avec fond noir
                    pdf.set_fill_color(0, 0, 0)  # Noir
                    pdf.set_text_color(255, 255, 255)  # Blanc
                    pdf.set_font("Arial", "B", 9)
                    pdf.cell(
                        30, 8, "Matricule", 1, 0, "C", fill=True
                    )  # Largeur ajustée
                    pdf.cell(75, 8, "Noms", 1, 0, "C", fill=True)  # Largeur ajustée
                    pdf.cell(20, 8, "Genre", 1, 0, "C", fill=True)  # Largeur ajustée
                    pdf.cell(
                        40, 8, "Date et lieu de nais.", 1, 0, "C", fill=True
                    )  # Largeur ajustée
                    pdf.cell(35, 8, "Tel", 1, 1, "C", fill=True)  # Largeur ajustée

                    # Liste des étudiants
                    pdf.set_fill_color(255, 255, 255)  # Fond blanc
                    pdf.set_text_color(0, 0, 0)  # Texte noir
                    for student in students:
                        matricule = (
                            str(student.matricule) if student.matricule else "N/A"
                        )
                        names = str(student.names) if student.names else "N/A"
                        gender = str(student.gender) if student.gender else "N/A"
                        birth_date = (
                            str(student.date_and_place_of_birth)
                            if student.date_and_place_of_birth
                            else "N/A"
                        )
                        phone = str(student.phone) if student.phone else "N/A"

                        pdf.cell(30, 8, matricule, 1, 0, "C")
                        pdf.cell(75, 8, names, 1, 0, "L")
                        pdf.cell(20, 8, gender, 1, 0, "L")
                        pdf.cell(40, 8, birth_date, 1, 0, "C")
                        pdf.cell(
                            35, 8, phone, 1, 1, "C"
                        )  # Nouvelle ligne après chaque étudiant

                    pdf.ln(5)
        pdf.ln(9)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0,10,f"Secrétaire Général",0,1,"L",)

        # Sauvegarder le PDF dans un fichier temporaire
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer, dest="S")
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="etudiants_{year}.pdf"'
        return response
