from django.contrib import admin
from .models import TypeProjet, Affectation, Prevision

@admin.register(TypeProjet)
class TypeProjectAdmin(admin.ModelAdmin):
    search_fields =["name",]

@admin.register(Affectation)
class AffectionAdmin(admin.ModelAdmin):
    list_display = [
        "teacher",
        "matricule",
        "student",
        "management_fees",
        "deposit_fees",
        "teacher_amount_collected",
        "section_sigle",
        "academic_year",
    ]
    search_fields = ["teacher__matricule", "teacher__name","student","matricule"]
    autocomplete_fields = [
        "teacher",
        "section",
        "promotion",
        "academic_year",
        "affected_by",
    ]
    list_filter = [
        "teacher",
        "section",
        "promotion",
        "academic_year",
    ]

    def section_sigle(self, obj):
        return obj.section.sigle
    section_sigle.short_description = "Section"

@admin.register(Prevision)
class PrevisionAdmin(admin.ModelAdmin):
    list_display = ["promotion", "deposit_fees", "management_fees", "academic_year"]
    list_filter = ["promotion", "academic_year"]
