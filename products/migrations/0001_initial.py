# Generated by Django 4.2 on 2023-05-06 12:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(default=None, null=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity_stock", models.IntegerField()),
                ("is_available_for_sale", models.BooleanField(default=False)),
                ("brand", models.CharField(max_length=50, null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Eletronics", "Eletronics"),
                            ("Clothing", "Clothing"),
                            ("Shoes", "Shoes"),
                            ("Toys", "Toys"),
                            ("Sports", "Sports"),
                            ("Health", "Health"),
                            ("School", "School"),
                            ("Books", "Books"),
                            ("Crafts", "Crafts"),
                            ("Home", "Home"),
                            ("Beauty", "Beauty"),
                            ("Garden", "Garden"),
                            ("Grocery", "Grocery"),
                            ("Others", "Others"),
                        ],
                        default="Others",
                        max_length=50,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]
