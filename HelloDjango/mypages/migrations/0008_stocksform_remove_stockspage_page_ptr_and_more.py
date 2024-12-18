# Generated by Django 5.1.3 on 2024-11-17 19:23

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mypages", "0007_alter_stockspage_intro_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StocksForm",
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
                (
                    "title",
                    models.CharField(
                        help_text="Название формы для админки", max_length=255
                    ),
                ),
                (
                    "success_message",
                    wagtail.fields.RichTextField(
                        blank=True, help_text="Сообщение после успешной отправки"
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="stockspage",
            name="page_ptr",
        ),
        migrations.CreateModel(
            name="StocksFormSubmission",
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
                ("name", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=20)),
                ("agreement", models.BooleanField(default=False)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "form",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="mypages.stocksform",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="StocksFormField",
        ),
        migrations.DeleteModel(
            name="StocksPage",
        ),
    ]
