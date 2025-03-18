from django.db import models
from student.models import Student
from parameter.models import Speciality,AcademicYear
from teacher.models import Teacher

class TypeProject(models.Model):
    name = models.CharField(max_length=50,verbose_name="Nom")
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Type Projet"
        verbose_name_plural = "Types de projets"
        db_table = "tfc_types"

class Proposition(models.Model):
    students = models.ManyToManyField(Student,related_name="propositon_student_set",verbose_name="Etudiants")
    type_projet = models.ForeignKey(TypeProject,on_delete=models.PROTECT,related_name="type_projet_proposition_set",null=True,blank=True,verbose_name="Type projet")