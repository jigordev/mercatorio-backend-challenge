# Generated by Django 5.2.1 on 2025-05-26 19:18

import django.db.models.deletion
import uuid6
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("credores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Certidao",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid6.uuid7,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("federal", "federal"),
                            ("estadual", "estadual"),
                            ("municipal", "municipal"),
                            ("trabalhista", "trabalhista"),
                        ]
                    ),
                ),
                (
                    "origem",
                    models.CharField(choices=[("manual", "manual"), ("api", "api")]),
                ),
                ("arquivo", models.FileField(upload_to="certidoes/")),
                ("arquivo_url", models.URLField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("negativa", "negativa"),
                            ("positiva", "positiva"),
                            ("invalida", "invalida"),
                            ("pendente", "pendente"),
                        ]
                    ),
                ),
                ("recebida_em", models.DateTimeField(auto_now_add=True)),
                (
                    "credor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certidoes",
                        to="credores.credor",
                    ),
                ),
            ],
        ),
    ]
