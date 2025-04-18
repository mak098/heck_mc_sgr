from django.contrib import admin
from .models import TypeProjet,Affectation

@admin.register(TypeProjet)
class TypeProjectAdmin(admin.ModelAdmin):
    search_fields =["name",]

@admin.register(Affectation)
class AffectionAdmin(admin.ModelAdmin):
    list_display = ["teacher", "student", "section", "academic_year"]
    search_fields = ["teacher__matricule", "teacher__name","student"]
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
