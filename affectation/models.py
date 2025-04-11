from django.db import models
from django.conf import settings
from teachers.models import Teacher
from student.models import Student
from parameter.models import AcademicYear,Section,Promotion

class TypeProjet(models.Model):
    name = models.CharField(max_length=25,primary_key=True,verbose_name="Nom")

    def __str__(self):
        return f"{self.name}"

class Affectation(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="affectations_teacher_set",
        verbose_name="Enseignants",
    )
    section = models.ForeignKey(Section,null=True,blank=True,on_delete=models.PROTECT,related_name="affectation_section_set",verbose_name="Section")    
    promotion = models.ForeignKey(
        Promotion,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="affectation_promotion_set",
        verbose_name="Promotion",
    )
    student = models.CharField(max_length=100,default="-",verbose_name="Nom du groupe")    
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="affectation_academic_year_set",
        verbose_name="Année academique",
    )    
    affected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="affectation_created_by_set",
        verbose_name="Utilisateur",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return f"{self.teacher.matricule} {self.teacher.first_name}"

    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
        db_table = "affectations"
