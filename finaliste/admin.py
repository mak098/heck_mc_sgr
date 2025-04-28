from django.contrib import admin
from .models import Finaliste
from import_export.admin import ImportExportModelAdmin
@admin.register(Finaliste)
class FinalisteAdmin(ImportExportModelAdmin):
    list_display = [
        "matricule",
        "names",
        "gender",
        "phone",
        "email",
        "orientation",
        "academic_year",
        "promotion",
    ]
    search_fields = [
        "matricule",
        "names",
        "phone",
        "email",
    ]
    autocomplete_fields = ["orientation", "academic_year", "promotion"]
    list_filter = [
        "gender",
        "orientation__section",
        "orientation",
        "promotion",
        "academic_year",
    ]
    fieldsets = (
        (
            "Identités de l'etudiant",
            {
                "fields": (
                    ("matricule", "names"),
                    ("date_and_place_of_birth"),
                    ("gender", "nationality"),
                )
            },
        ),
        (
            "Contacts",
            {"fields": (("phone", "email"),)},
        ),
        (
            "Profession",
            {"fields": (("previous_training", "status"),)},
        ),
        (
            "Info Academique",
            {"fields": (("orientation", "promotion", "academic_year"),)},
        ),
        
    )
