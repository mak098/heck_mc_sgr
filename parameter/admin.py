from django.contrib import admin
from .models import AcademicYear, Section,Filiere, DocumentFolde, Promotion, Firm, Speciality

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
