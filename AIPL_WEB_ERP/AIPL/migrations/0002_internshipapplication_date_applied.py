# Generated by Django 5.1.2 on 2024-11-17 18:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIPL', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipapplication',
            name='date_applied',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time when the application was submitted.'),
        ),
    ]