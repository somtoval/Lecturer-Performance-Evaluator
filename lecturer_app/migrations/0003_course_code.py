# Generated by Django 5.1.4 on 2025-05-07 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lecturer_app", "0002_remove_lecturer_user_lecturer_name_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="code",
            field=models.CharField(default="Unknown mycoursecode", max_length=255),
            preserve_default=False,
        ),
    ]
