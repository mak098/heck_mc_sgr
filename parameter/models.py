from django.db import models
from django.conf import settings

class AcademicYear(models.Model):
    year = models.CharField(max_length=10,unique=True,primary_key=True,verbose_name="Année")
    is_current = models.BooleanField(default=False,verbose_name="Active")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="academic_yer_created_by_set",
        verbose_name="Utilisateur",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return f"{self.year}"

    class Meta:
        verbose_name = "Années Academique"
        verbose_name_plural = "Année Academique"
        db_table = "academic_year"

class Filiere(models.Model):
    name = models.CharField(max_length=256,verbose_name="Filière")
    code = models.CharField(max_length=20, null=True,blank=True,verbose_name="Code")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="filiere_created_by_set",
        verbose_name="Utilisateur",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Orientations"
        verbose_name_plural = "Orientation"
        db_table = "filieres"

class DocumentFolde(models.Model):
    name = models.CharField(max_length=256,verbose_name="Nom")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="document_created_by_set",
        verbose_name="Utilisateur",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Elements du dossier"
        verbose_name_plural = "Element du dossier"
        db_table = "documents_folde"
