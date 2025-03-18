from django.db import models
from django.conf import settings

class Firm(models.Model):
    name = models.CharField(max_length=256,verbose_name="Nom")
    sigle = models.CharField(max_length=25,default='-',verbose_name="Sigle")
    service = models.CharField(max_length=256, verbose_name="Service")
    service_sigle = models.CharField(max_length=256, verbose_name="Service sigle")
    email = models.CharField(max_length=256,verbose_name="Email")
    phone = models.CharField(max_length=256,verbose_name="Phone")
    logo = models.ImageField(upload_to='logo/etablissement/',verbose_name="Logo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Etablissement"
        verbose_name_plural = "Etablissement"
        db_table = "etablishements"

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
        verbose_name = "Année Academique"
        verbose_name_plural = "Années Academique"
        db_table = "academic_year"

class Section(models.Model):
    sigle = models.CharField(max_length=50,unique=True,verbose_name="Sigle")
    name = models.CharField(max_length=250, unique=True,verbose_name="Nom")
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        db_table = "sections"

class Filiere(models.Model):
    section = models.ForeignKey(Section,related_name="filiere_section_set", on_delete=models.PROTECT,null=True,verbose_name="Section")
    name = models.CharField(max_length=256,verbose_name="Filière")
    code = models.CharField(max_length=20, null=True,blank=True,verbose_name="Code")
    sigle = models.CharField(max_length=50,default="-",verbose_name="Sigle")
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
        verbose_name = "Orientation"
        verbose_name_plural = "Orientations"
        db_table = "filieres"

class Speciality(models.Model):
    name = models.CharField(max_length=300,verbose_name="nom")
    orientation = models.ForeignKey(Filiere,on_delete=models.PROTECT,related_name="specialities_filiere_set",verbose_name="Orientation")
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Specialité"
        verbose_name_plural = "Specialités"
        db_table = "specialities"
class Promotion(models.Model):
    code = models.CharField(
        max_length=50,
        default="-",
        null=False,
        blank=False,
        unique=True,
        verbose_name="code"
    )
    name = models.CharField(
        max_length=150, null=False, blank=False,unique=True, verbose_name="Nom"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F"{self.name}"
    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        db_table = "promotions"


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
        verbose_name = "Element du dossier"
        verbose_name_plural = "Elements du dossier"
        db_table = "documents_folde"
