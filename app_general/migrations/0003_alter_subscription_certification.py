# Generated by Django 5.0.4 on 2024-05-03 04:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_certifications', '0001_initial'),
        ('app_general', '0002_subscription_certification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='certification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_certifications.certification'),
        ),
    ]
