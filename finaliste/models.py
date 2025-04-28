from django.db import models
from django.conf import settings
from parameter.models import Filiere, AcademicYear, DocumentFolde, Promotion


class Finaliste(models.Model):
    matricule = models.CharField(max_length=25, unique=True, verbose_name="Matricule")
    names = models.CharField(max_length=100, verbose_name="Noms")
    # date_of_birth = models.CharField(max_length=25,verbose_name="Date de naissance")
    date_and_place_of_birth = models.CharField(
        max_length=100, verbose_name="Lieu de naissance"
    )
    gender = models.CharField(
        max_length=10,
        default="Masculin",
        choices=(("Masculin", "Masculin"), ("Féminin", "Féminin")),
        verbose_name="Sexe",
    )
    nationality = models.CharField(
        max_length=256, default="Congolaise", verbose_name="Nationalité"
    )
    previous_training = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="FORMATION ANTERIEURE"
    )
    status = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Statut"
    )
    phone = models.CharField(
        max_length=25, null=True, blank=True, verbose_name="TELEPHONE"
    )
    email = models.EmailField(
        max_length=150, null=True, blank=True, verbose_name="Email"
    )
    orientation = models.ForeignKey(
        Filiere,
        on_delete=models.PROTECT,
        related_name="finalist_orientation_set",
        verbose_name="Orientation",
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.PROTECT,
        null=True,
        related_name="finalist_promotion_set",
        verbose_name="Promotion",
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="finalist_acadmic_year_set",
        verbose_name="Année academique",
    )
   

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="finalist_created_by_set",
        verbose_name="Utilisateur",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.matricule} {self.names}"

    class Meta:
        verbose_name = "Finaliste"
        verbose_name_plural = "Finalistes"
        db_table = "finaliste"
