# Generated by Django 4.0.6 on 2024-09-12 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AIPL', '0006_newsarticle_subscribers'),
    ]

    operations = [
        migrations.CreateModel(
            name='developer_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_role', models.CharField(choices=[('Frontend Dev', 'Frontend Dev'), ('Backend Dev', 'Backend Dev'), ('DevOps Eng', 'DevOps Eng'), ('Fullstack Dev', 'Fullstack Dev'), ('AA Dev', 'AA Dev'), ('IOS Dev', 'IOS Dev'), ('Software Dev', 'Software Dev'), ('AI/ML Eng', 'AI/ML Eng'), ('Data Analyst', 'Data Analyst'), ('DB Admin', 'DB Admin'), ('Cloud Dev', 'Cloud Dev'), ('Blockchain Dev', 'Blockchain Dev'), ('AR/VR Dev', 'AR/VR Dev'), ('Test Automation', 'Test Automation')], max_length=50)),
                ('points', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('developer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Devloper Panel',
                'verbose_name_plural': 'Devloper Panel',
            },
        ),
    ]
