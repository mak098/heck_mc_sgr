from django.http import HttpResponse
from fpdf import FPDF
from io import BytesIO
from django.db.models import Sum, F, FloatField
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Prefetch
from rest_framework import viewsets
from datetime import datetime
from parameter.models import AcademicYear,Filiere,Promotion
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

class exportPdfByAcademicYear(viewsets.ModelViewSet):

    def get_pdf_for_all_section_in_by_year(self, request, year):
        academic = AcademicYear.objects.get(year=year)

        filiers = Filiere.objects.all()
        for filier in filiers:
            pass

