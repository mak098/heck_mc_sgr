from django.contrib import admin
from .models import Teacher,Grade
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from import_export import resources, widgets, fields
from import_export.widgets import ForeignKeyWidget



@admin.register(Grade)
class GradeAdmin(ImportExportModelAdmin):
    list_display = ["grade", "number_of_hours"]
    search_fields = ["grade"]


class GradeWidget(ForeignKeyWidget):
    """Widget pour rechercher ou créer grade par grade"""

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        obj, created = Grade.objects.get_or_create(grade=value)
        return obj


class GradeResource(resources.ModelResource):

    grade = fields.Field(
        column_name="grade",
        attribute="grade",
        widget=GradeWidget(Grade, "grade"),
    )
    class Meta:
        model = Teacher
        import_id_fields = ("grade_enseignant",)  


@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin, DjangoUserAdmin):
   
    list_display = [
        "grade",
        "matricule",
        "first_name",
        "last_name",
        "name",
    ]
    list_filter = ["grade", "section"]
    search_fields = ["matricule",  "first_name", "last_name"]
    autocomplete_fields = ["section","grade"]
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
                    "section",
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
    filter_horizontal = ("groups",)
