from django.db import models
from authentication.models import User
from parameter.models import Section,Speciality
from django.conf import settings

class Grade(models.Model):
    '''Qualifications des enseignants'''
    title = models.CharField(max_length=150,unique=True, verbose_name="Titre")
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
        return f"{self.title}"

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        db_table = "grades"

class Teacher(User):
    matricule = models.CharField(
        max_length=25, unique=True, verbose_name="Matricule"
    )
    name = models.CharField(max_length=25, null=True, blank=True, verbose_name="Matricule")
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name="Nom")
    type = models.CharField(
        max_length=25, default="permanant",choices=(
            ("permanent","Permenant"),
            ("visiteur","visiteur")
        ), null=True, blank=True, verbose_name="Type"
    )
    section = models.ForeignKey(
        Section,
        null=True,blank=True,
        on_delete=models.PROTECT,
        related_name="teacher_orientation_set_set",
        verbose_name="Orientation",
    )
    grade = models.ForeignKey(
        Grade, on_delete=models.PROTECT,null=True,blank=True,related_name="teacher_grade_set", verbose_name="Grade"
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

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        db_table = "teachers"

class TeacherSpeciality(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.PROTECT,related_name="teacher_speciality_set",verbose_name="Enseignant")
    speciality = models.ForeignKey(Speciality,on_delete=models.PROTECT,related_name="speciality_teacher_set",verbose_name="Specialité")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.teacher} {self.speciality}"

    class Meta:
        verbose_name = "Enseignant et specialité"
        verbose_name_plural = "Enseignants et specialiés"
        db_table = "teachers_specialities"