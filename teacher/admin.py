from django.contrib import admin
from .models import Teacher,Grade
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["title", "number_of_hours"]
    search_fields = ["title"]

@admin.register(Teacher)
class TeacherAdmin(DjangoUserAdmin):
    list_display = [
        "grade",
        "matricule",
        "first_name",
        "last_name",
        "email",
        "orientation",
    ]
    list_filter = ["grade", "orientation"]
    search_fields = ["matricule",  "first_name", "last_name"]
    autocomplete_fields = ["orientation","grade"]
    fieldsets = (
        (
            "identifier",
            {
                "fields": ("username", "password"),
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "matricule",
                    "first_name",
                    "last_name",
                    "name",
                    "email",
                    "phone",
                ),
            },
        ),
        (
            "Information academique",
            {
                "fields": (
                    "grade",
                    "orientation",
                    "specialities"
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups"),
            },
        ),
        
    )
    filter_horizontal = ("groups","specialities")
