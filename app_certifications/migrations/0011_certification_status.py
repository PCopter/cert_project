# Generated by Django 5.0.4 on 2024-05-21 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_certifications', '0010_remove_certification_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='status',
            field=models.CharField(choices=[('activate', 'Activate'), ('risk', 'Risk'), ('alert', 'Alert')], default='activate', max_length=10),
        ),
    ]