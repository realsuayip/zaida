# Generated by Django 4.2.9 on 2024-01-14 19:14

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("account", "0008_user_language"),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.group",),
            managers=[
                ("objects", django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.permission",),
            managers=[
                ("objects", django.contrib.auth.models.PermissionManager()),
            ],
        ),
    ]