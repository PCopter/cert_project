# Generated by Django 5.0.4 on 2024-05-18 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_certifications', '0004_certification_expire_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='status',
            field=models.CharField(choices=[('activating', 'Activating'), ('risk', 'Risk'), ('alert', 'Alert')], default='activating', max_length=15),
        ),
    ]
