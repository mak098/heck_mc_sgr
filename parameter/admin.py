from django.contrib import admin
from .models import AcademicYear, Section,Filiere, DocumentFolde, Promotion, Firm, Speciality
from ui.rapportTeacherPdf import ExportPdf
from .views import (
    getAllTeacherStudentBySectionExcel,
    downloadStudentsByAcademicYearExcel,
)


def download_students_by_academic_year(modeladmin, request, queryset):
    return downloadStudentsByAcademicYearExcel(request, queryset.values())


def download_deposity_fees(modeladmin, request, queryset):
    return ExportPdf.getAllTeacherPayementDepositSyntheseBySection(
        request, queryset.values()
    )
def download_affection(modeladmin, request, queryset):
    return ExportPdf.getAllTeacherStudentBySection(request, queryset.values())
def download_affection_sythese(modeladmin, request, queryset):
    return ExportPdf.getAllTeacherPayementSyntheseBySection(request, queryset.values())
def download_affection_sythese_excel(modeladmin, request, queryset):
    return ExportPdf.getAllTeacherPayementSyntheseBySectionExcel(
        request, queryset.values()
    )
def download_affection_excel(modeladmin, request, queryset):
    return getAllTeacherStudentBySectionExcel(request, queryset.values())

download_deposity_fees.short_description = "telecharger frais de depot"
download_affection.short_description = "telecharger les etudiant actuel"
download_affection_sythese.short_description = "telecharger synthese paiement"
download_affection_sythese_excel.short_description = "telecharger synthese paiement excel"
download_affection_excel.short_description = "telecharger les etudiant actuel en excel"
download_students_by_academic_year.short_description = (
    "telecharger les etudiants par annee academique"
)


class FiliereInline(admin.TabularInline):
    extra = 0
    model = Filiere
    fields = ["name", "sigle", "code"]

class SpecialityInline(admin.TabularInline):
    extra = 0
    model = Speciality
    fields = ["name",]

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin): 

    search_fields = ("name",)
@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
    pass


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ["year", "is_current"]
    fields = ["year", "is_current"]
    search_fields = ["year"]
    actions = [download_students_by_academic_year]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code"]
    fields = ["name", "code"]
    search_fields = ["name", "code"]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sigle"]
    fields = [ "name", "sigle"]
    search_fields = ["name", "sigle"]
    inlines = [FiliereInline,]
    actions = [
        download_affection,
        download_affection_sythese,
        download_affection_sythese_excel,
        download_affection_excel,
        download_deposity_fees,
    ]

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sigle", "code", "section"]
    fields = ["section", "name", "sigle", "code"]
    search_fields = ["name", "sigle", "code"]
    inlines = [SpecialityInline,]
    list_filter =["section"]
    autocomplete_fields = ["section"]
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()
@admin.register(DocumentFolde)
class DocumentFoldeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name"]
    search_fields = ["name"]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()
