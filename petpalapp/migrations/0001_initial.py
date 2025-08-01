# Generated by Django 5.2 on 2025-07-26 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('original_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('image', models.ImageField(upload_to='accessories/')),
                ('category', models.CharField(choices=[('Collar', 'Collar'), ('Leash', 'Leash'), ('Toy', 'Toy'), ('Bowl', 'Bowl'), ('Bed', 'Bed'), ('Clothes', 'Clothes'), ('Food', 'Food'), ('Other', 'Other')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='breed/')),
                ('life_span', models.CharField(default='10-12 years', max_length=30)),
                ('size', models.CharField(default='Medium', max_length=20)),
                ('weight', models.CharField(default='Unknown', max_length=20)),
                ('height', models.CharField(default='Unknown', max_length=20)),
                ('exercise', models.CharField(default='Unknown', max_length=20)),
                ('grooming', models.CharField(default='unknown', max_length=20)),
                ('overview', models.TextField(default='No overview available at this time.')),
                ('good_with_kids', models.BooleanField(default=True)),
                ('energy_level', models.CharField(default='Medium', max_length=50)),
                ('ease_of_training', models.CharField(default='Moderate', max_length=50)),
                ('grooming_requirement', models.CharField(default='Medium', max_length=50)),
                ('vocality', models.CharField(default='Medium', max_length=50)),
                ('affection_needs', models.CharField(default='Moderate', max_length=50)),
                ('exercise_requirement', models.CharField(default='Medium', max_length=50)),
            ],
        ),
    ]
