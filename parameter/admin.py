from django.contrib import admin
from .models import AcademicYear,Filiere,DocumentFolde,Promotion

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
    list_display = ["id","name"]
    fields = ["name"]
    search_fields = ["name"]
@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ["id","name", "code"]
    fields = ["name", "code"]
    search_fields = ["name","code"]
    
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
