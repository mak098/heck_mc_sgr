from django.contrib import admin
from .models import Student,AttachementFile
from import_export.admin import ImportExportModelAdmin
from .views import download_students_excel


def download_student(modeladmin, request, queryset):
    return download_students_excel(request, queryset.values())
download_student.short_description = "telecharger les etudiant actuel"

class AttachementInline(admin.TabularInline):
    model = AttachementFile
    fields = ['name','file']
    extra = 0
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    actions = [download_student,]
    list_display = [
        "matricule",
        "names",
        "gender",
        "phone",
        "email",
        "orientation",
        "academic_year",
        "promotion"
    ]
    search_fields =  [
        "matricule",
        "names",
        "phone",
        "email",        
    ]
    autocomplete_fields = [
        "orientation",
        "academic_year",
        "promotion"
    ]
    list_filter = ["gender", "orientation__section", "orientation", "promotion", "academic_year"]
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
            {"fields": (("orientation","promotion", "academic_year"),)},
        ),
        (
            "Documents",
            {
                "fields": (
                    "documents",
                    "scan_file",
                )
            },
        ),
    )
    inlines = [AttachementInline,]
    filter_horizontal = ["documents",]

@admin.register(AttachementFile)
class AttachementAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ["student","name", "file", ]
    search_fields = ['name']
