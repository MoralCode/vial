# Generated by Django 3.1.7 on 2021-03-23 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0048_delete_test_reports"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="is_test_data",
        ),
        migrations.RemoveField(
            model_name="report",
            name="is_test_data",
        ),
    ]
