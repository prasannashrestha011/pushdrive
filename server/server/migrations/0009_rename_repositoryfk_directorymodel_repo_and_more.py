# Generated by Django 5.2 on 2025-04-06 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0008_usermodel_folder_link"),
    ]

    operations = [
        migrations.RenameField(
            model_name="directorymodel",
            old_name="repositoryFK",
            new_name="repo",
        ),
        migrations.RenameField(
            model_name="filemodel",
            old_name="directoryFk",
            new_name="directory",
        ),
        migrations.RenameField(
            model_name="filemodel",
            old_name="repositoryFK",
            new_name="repository",
        ),
        migrations.RemoveField(
            model_name="directorymodel",
            name="dirLink",
        ),
        migrations.RemoveField(
            model_name="directorymodel",
            name="dirName",
        ),
        migrations.RemoveField(
            model_name="filemodel",
            name="fileLink",
        ),
        migrations.RemoveField(
            model_name="repositorymodel",
            name="repoLink",
        ),
    ]
