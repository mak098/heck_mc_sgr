# Generated by Django 5.0.1 on 2025-03-04 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0006_firm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='nom')),
                ('orientation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='specialities_filiere_set', to='parameter.filiere', verbose_name='Orientation')),
            ],
            options={
                'verbose_name': 'Specialité',
                'verbose_name_plural': 'Specialités',
                'db_table': 'specialities',
            },
        ),
    ]
