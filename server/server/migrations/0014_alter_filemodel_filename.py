# Generated by Django 5.2 on 2025-04-08 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0013_directorymodel_dirname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filemodel",
            name="fileName",
            field=models.CharField(max_length=255),
        ),
    ]
