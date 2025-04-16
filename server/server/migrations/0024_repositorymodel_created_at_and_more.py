# Generated by Django 5.2 on 2025-04-16 06:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0023_alter_userstoragereference_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="repositorymodel",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repositorymodel",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
