from django.db import models
from authentication.models import User
from parameter.models import Section,Speciality
from django.conf import settings

class Grade(models.Model):
    '''Qualifications des enseignants'''
    grade = models.CharField(max_length=150,primary_key=True,unique=True, verbose_name="grade")
    description = models.CharField(max_length=256,null=True,blank=True,verbose_name="description")
    number_of_hours = models.FloatField(max_length=10,default=0,verbose_name="Nombre d'heures de prestation")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="teacher_grade_created_by",
        verbose_name="Created by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return f"{self.grade}"

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        db_table = "gradess"

class Teacher(User):
    matricule = models.CharField(
        max_length=25, unique=True, verbose_name="Matricule"
    )
    name = models.CharField(max_length=25, null=True, blank=True, verbose_name="nom")
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name="Phone")
    type = models.CharField(
        max_length=25, default="permanant",choices=(
            ("permanent","Permenant"),
            ("visiteur","visiteuu")
        ), null=True, blank=True, verbose_name="Type"
    )
    section = models.ForeignKey(
        Section,
        null=True,blank=True,
        on_delete=models.PROTECT,
        related_name="teacher_sections_set",
        verbose_name="Orientation",
    )
    grade = models.ForeignKey(
        Grade, on_delete=models.PROTECT,null=True,blank=True,related_name="teacher_grades_set", verbose_name="Grade"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        db_table = "tb_teachers"
