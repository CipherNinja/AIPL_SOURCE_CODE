# Generated by Django 4.0.6 on 2024-07-26 15:17

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
            name='dataDeletionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('privacy concern', 'Privacy Concern'), ('security concern', 'Security Concern'), ('no longer needed', 'No Longer Needed'), ('regulatory request (e.g. gdpr/ccpa)', 'Regulatory Request (e.g. GDPR/CCPA)'), ('other', 'Other')], max_length=55)),
                ('additional_info', models.TextField(max_length=1500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
