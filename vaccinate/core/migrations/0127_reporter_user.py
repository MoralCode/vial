# Generated by Django 3.2.1 on 2021-05-11 00:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0126_sourcelocation_source_loca_matched_d1b866_idx"),
    ]

    operations = [
        migrations.AddField(
            model_name="reporter",
            name="user",
            field=models.ForeignKey(
                blank=True,
                help_text="Corresponding user record for this reporter",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="reporters",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
