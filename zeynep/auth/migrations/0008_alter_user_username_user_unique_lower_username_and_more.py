# Generated by Django 4.1 on 2022-08-07 11:20

import django.core.validators
from django.db import migrations, models
import django.db.models.functions.text
import zeynep.auth.models.user


class Migration(migrations.Migration):

    dependencies = [
        ("zeynep_auth", "0007_user_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=16,
                validators=[
                    django.core.validators.MinLengthValidator(3),
                    zeynep.auth.models.user.UsernameValidator(),
                ],
                verbose_name="username",
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("username"),
                name="unique_lower_username",
                violation_error_message="The username you specified is already in use.",
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("username__regex", "^[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*$")
                ),
                name="regex_valid_username",
                violation_error_message="Usernames can only contain latin letters, numerals and underscores. Trailing, leading or consecutive underscores are not allowed.",
            ),
        ),
    ]