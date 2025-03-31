from django.contrib import admin
from .models import TypeProjet,Affectation

@admin.register(TypeProjet)
class TypeProjectAdmin(admin.ModelAdmin):
    search_fields =["name",]

@admin.register(Affectation)
class AffectionAdmin(admin.ModelAdmin):
    list_display = ["teacher", "student", "type", "academic_year"]
    autocomplete_fields = [
        "teacher",
        "type",
        "student",
        "academic_year",
        "affected_by",
    ]
    list_filter = [
        "teacher",
        "type",
        "academic_year",
    ]
