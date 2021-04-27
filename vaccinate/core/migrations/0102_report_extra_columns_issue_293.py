# Generated by Django 3.1.8 on 2021-04-24 01:11

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0101_new_availability_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="full_address",
            field=models.TextField(
                blank=True,
                help_text="Update for the entire address, including city and zip code",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="report",
            name="hours",
            field=models.TextField(
                blank=True, help_text="Update for hours information", null=True
            ),
        ),
        migrations.AddField(
            model_name="report",
            name="planned_closure",
            field=models.DateField(
                blank=True,
                help_text="Date this site a site plans to stop operating",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="report",
            name="restriction_notes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="report",
            name="vaccines_offered",
            field=models.JSONField(
                blank=True,
                help_text="JSON array of strings representing vaccines on offer here",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="report",
            name="website",
            field=core.fields.CharTextField(
                blank=True,
                help_text="Update for website information",
                max_length=65000,
                null=True,
            ),
        ),
    ]
