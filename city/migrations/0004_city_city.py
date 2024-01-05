# Generated by Django 5.0.1 on 2024-01-04 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("city", "0003_remove_city_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="city",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cities_light.city",
            ),
        ),
    ]