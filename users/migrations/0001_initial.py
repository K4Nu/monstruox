# Generated by Django 4.2.13 on 2024-07-05 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Clan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=72, unique=True)),
                ("motto", models.CharField(max_length=256, unique=True)),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=2500, null=True, unique=True
                    ),
                ),
                ("creation_date", models.DateField(auto_now_add=True)),
                ("level", models.PositiveIntegerField(default=1)),
                ("experience", models.PositiveIntegerField(default=0)),
                (
                    "emblem",
                    models.ImageField(blank=True, null=True, upload_to="emblems/"),
                ),
                (
                    "leader",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nickname", models.CharField(max_length=60, unique=True)),
                ("bio", models.CharField(max_length=256, null=True)),
                ("credits", models.FloatField(default=0.0)),
                ("level", models.PositiveIntegerField(default=1)),
                ("experience", models.PositiveIntegerField(default=0)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="avatar/"),
                ),
                (
                    "clan",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.clan",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
