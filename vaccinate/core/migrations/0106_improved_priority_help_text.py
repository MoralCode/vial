# Generated by Django 3.1.8 on 2021-04-27 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0105_location_import_run"),
    ]

    operations = [
        migrations.AlterField(
            model_name="callrequest",
            name="priority",
            field=models.IntegerField(
                db_index=True,
                default=0,
                help_text="Priority within this priority group - higher number means higher priority",
            ),
        ),
    ]
