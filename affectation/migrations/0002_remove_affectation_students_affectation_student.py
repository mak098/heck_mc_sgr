# Generated by Django 5.0.1 on 2025-03-19 13:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affectation', '0001_initial'),
        ('student', '0004_alter_student_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affectation',
            name='students',
        ),
        migrations.AddField(
            model_name='affectation',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='affectations_students_set', to='student.student', verbose_name='Etudiants'),
            preserve_default=False,
        ),
    ]
