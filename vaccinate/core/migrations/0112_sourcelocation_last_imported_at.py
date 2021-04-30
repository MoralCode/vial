# Generated by Django 3.2 on 2021-04-30 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0111_populate_location_point"),
    ]

    operations = [
        migrations.AddField(
            model_name="sourcelocation",
            name="last_imported_at",
            field=models.DateTimeField(
                blank=True,
                help_text="When this source location was last imported",
                null=True,
            ),
        ),
    ]
