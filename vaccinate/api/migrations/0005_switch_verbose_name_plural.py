# Generated by Django 3.1.8 on 2021-04-15 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_enable_history_on_switch"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="switch",
            options={"verbose_name_plural": "Switches"},
        ),
    ]
