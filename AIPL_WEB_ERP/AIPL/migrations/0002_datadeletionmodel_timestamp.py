# Generated by Django 4.0.6 on 2024-07-27 22:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AIPL', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datadeletionmodel',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
