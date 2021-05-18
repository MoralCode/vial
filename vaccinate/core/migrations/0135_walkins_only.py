# Generated by Django 3.2.3 on 2021-05-18 05:27

from django.db import migrations


def fix_walkins(apps, schema_editor):
    AvailabilityTag = apps.get_model("core", "AvailabilityTag")
    AvailabilityTag.objects.filter(slug="walk_ins_accepted").update(
        slug="walk_ins_only",
        name="Walk-ins only",
        notes="This location only allows walkins",
        # We keep the "Yes: walk-in accepted" name, which is what older Scooby may submit.
        previous_names=["Yes: walk-ins accepted", "Walk-ins accepted"],
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0134_alter_location_created_at"),
    ]

    operations = [
        migrations.RunPython(fix_walkins, reverse_code=lambda apps, schema_editor: None)
    ]
