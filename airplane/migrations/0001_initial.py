# Generated by Django 5.0 on 2024-01-06 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("airline", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Airplane",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("seats", models.IntegerField()),
                ("model_number", models.CharField(max_length=10, unique=True)),
                (
                    "airline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airline.airline",
                    ),
                ),
            ],
        ),
    ]
