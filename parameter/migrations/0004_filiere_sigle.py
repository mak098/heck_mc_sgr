# Generated by Django 5.0.1 on 2025-02-28 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0003_promotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='filiere',
            name='sigle',
            field=models.CharField(default='-', max_length=50, verbose_name='Sigle'),
        ),
    ]
