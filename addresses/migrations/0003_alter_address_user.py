# Generated by Django 4.2 on 2023-05-03 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("addresses", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="address",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]