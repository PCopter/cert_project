# Generated by Django 5.0.4 on 2024-06-15 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_certifications', '0019_country_image_relative_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='alert_threshold',
            new_name='critical_threshold',
        ),
        migrations.RemoveField(
            model_name='country',
            name='risk_threshold',
        ),
        migrations.AddField(
            model_name='country',
            name='caution_threshold',
            field=models.IntegerField(default=90),
        ),
        migrations.AddField(
            model_name='country',
            name='serious_threshold',
            field=models.IntegerField(default=60),
        ),
        migrations.AlterField(
            model_name='certificatenumber',
            name='status',
            field=models.CharField(choices=[('activating', 'Activating'), ('caution', 'Caution'), ('serious', 'Serious'), ('critical', 'Critical')], default='activate', max_length=10),
        ),
        migrations.AlterField(
            model_name='certification',
            name='certificate_name',
            field=models.CharField(default='Please enter the certificate name. ', max_length=255),
        ),
    ]
