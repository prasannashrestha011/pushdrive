# Generated by Django 5.2 on 2025-04-09 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0016_userstoragedetails"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="userstoragedetails",
            table="users_storage_reference",
        ),
    ]
