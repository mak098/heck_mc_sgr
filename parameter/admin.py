from django.contrib import admin
from .models import AcademicYear, Filiere, DocumentFolde, Promotion, Firm, Speciality


class SpecialityInline(admin.TabularInline):
    extra = 0
    model = Speciality
    fields = ["name",]

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin): pass
@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
    pass


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ["year", "is_current"]
    fields = ["year", "is_current"]
    search_fields = ["year"]
    
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code"]
    fields = ["name", "code"]
    search_fields = ["name", "code"]
@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ["id","name","sigle", "code"]
    fields = ["name","sigle", "code"]
    search_fields = ["name", "sigle", "code"]
    inlines = [SpecialityInline,]

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
