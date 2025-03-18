from django.db import models
from parameter.models import AcademicYear

class Folder(models.Model):
    name = models.CharField(max_length=250, verbose_name="Nom")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Classeur"
        verbose_name_plural = "Classeurs"
        db_table = "packages"


class Letter(models.Model):
    folder = models.ForeignKey(Folder,on_delete=models.PROTECT,related_name="folder_file_set",verbose_name="CLASSEUR")
    ref = models.CharField(max_length=250,default='-',verbose_name="REF")
    object = models.CharField(max_length=250,default="-",verbose_name="OBJET/ RESUME")
    sender_or_reciver = models.CharField(max_length=200,null=True,blank=True, verbose_name="EXPEDITAIRE/ DESTINATAIRE")
    num_note = models.CharField(max_length=200,null=True,blank=True, verbose_name="NUMERO DE LA LETTRE")
    _date = models.DateField(verbose_name="DATE") 
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="file_package_set",
        verbose_name="ANNE ACADEMIQUE",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return f"{self.folder.name} {self.ref}"

    class Meta:
        verbose_name = "Lettre"
        verbose_name_plural = "Lettres"
        db_table = "leters"
