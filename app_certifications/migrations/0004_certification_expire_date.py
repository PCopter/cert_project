# Generated by Django 5.0.4 on 2024-05-14 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_certifications', '0003_certification_image_relative_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='expire_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
