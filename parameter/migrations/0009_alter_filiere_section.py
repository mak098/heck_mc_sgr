# Generated by Django 5.0.1 on 2025-03-05 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0008_section_filiere_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filiere',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='filiere_section_set', to='parameter.section', verbose_name='Section'),
        ),
    ]
