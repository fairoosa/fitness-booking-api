# Generated by Django 5.2.3 on 2025-06-27 18:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user_management", "0002_classtype_created_at_classtype_updated_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="classtype",
            old_name="name",
            new_name="class_name",
        ),
    ]
