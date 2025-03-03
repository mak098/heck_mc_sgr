from django.db import models
from authentication.models import User
from parameter.models import Filiere
from parameter.models import TeacherQualification
from django.conf import settings

class Grade(models.Model):
    '''Qualifications des enseignants'''
    title = models.CharField(max_length=150,unique=True, verbose_name="Titre")
    number_of_hours = models.FloatField(max_length=10, verbose_name="Nombre d'heures de prestation")
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
        return f"{self.title}"

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        db_table = "grades"

class Teacher(User):
    matricule = models.CharField(
        max_length=25, unique=True, verbose_name="Matricule"
    )
    name = models.CharField(max_length=25, null=True, blank=True, verbose_name="Nom")
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name="Phone")
    type = models.CharField(
        max_length=25, default="permanant", null=True, blank=True, verbose_name="Type"
    )
    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.PROTECT,
        related_name="section_set",
        verbose_name="Section",
    )
    grade = models.ForeignKey(
        Grade, on_delete=models.PROTECT,related_name="teacher_grade_set", verbose_name="Grade"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="teacher_created_by",
        verbose_name="Created by",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def fullname(self):
        return f"{self.first_name} {self.last_name} {self.name}"

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        db_table = "teacher"
