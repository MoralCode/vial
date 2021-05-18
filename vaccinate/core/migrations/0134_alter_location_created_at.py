# Generated by Django 3.2.3 on 2021-05-18 01:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0133_backfill_location_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
