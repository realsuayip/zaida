# Generated by Django 4.2.16 on 2024-11-02 20:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0012_proxy_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="userdeactivation",
            name="for_deletion",
            field=models.BooleanField(
                default=False,
                help_text="Marks this user's account for permanent deletion.",
                verbose_name="for deletion",
            ),
        ),
    ]