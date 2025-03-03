# Generated by Django 5.0.1 on 2025-03-03 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0005_promotion_code_alter_promotion_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nom')),
                ('sigle', models.CharField(default='-', max_length=25, verbose_name='Sigle')),
                ('service', models.CharField(max_length=256, verbose_name='Service')),
                ('service_sigle', models.CharField(max_length=256, verbose_name='Service sigle')),
                ('email', models.CharField(max_length=256, verbose_name='Email')),
                ('phone', models.CharField(max_length=256, verbose_name='Phone')),
                ('logo', models.ImageField(upload_to='logo/etablissement/', verbose_name='Logo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Etablissement',
                'verbose_name_plural': 'Etablissement',
                'db_table': 'etablishements',
            },
        ),
    ]
