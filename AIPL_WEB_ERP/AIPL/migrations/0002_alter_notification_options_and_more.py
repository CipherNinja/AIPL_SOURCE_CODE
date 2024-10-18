# Generated by Django 4.0.6 on 2024-10-18 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIPL', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={},
        ),
        migrations.AlterField(
            model_name='developer_profile',
            name='job_role',
            field=models.CharField(choices=[('Frontend Dev', 'Frontend Dev'), ('Backend Dev', 'Backend Dev'), ('DevOps Eng', 'DevOps Eng'), ('Fullstack Dev', 'Fullstack Dev'), ('IOS Dev', 'IOS Dev'), ('Software Dev', 'Software Dev'), ('AI/ML Eng', 'AI/ML Eng'), ('Data Analyst', 'Data Analyst'), ('DB Admin', 'DB Admin'), ('Cloud Dev', 'Cloud Dev'), ('Blockchain Dev', 'Blockchain Dev'), ('AR/VR Dev', 'AR/VR Dev'), ('Test Automation', 'Test Automation'), ('BDA Trainee', 'BDA Trainee'), ('Content Writer', 'Content Writer'), ('Digital Marketing Trainee', 'Digital Marketing Trainee'), ('Backend Dev .Net', 'Backend Dev .Net'), ('Backend Dev PHP', 'Backend Dev PHP'), ('Database Administrator', 'Database Administrator'), ('SDE with Java', 'SDE with Java'), ('Business Development Analyst', 'Business Development Analyst'), ('Head | Human Resources', 'Head | Human Resources'), ('Director IT', 'Director IT'), ('CEO', 'CEO'), ('Deputy Director', 'Deputy Director')], max_length=50),
        ),
    ]
