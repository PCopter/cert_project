# Generated by Django 5.0.4 on 2024-05-21 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_certifications', '0012_remove_certification_remark_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='expire_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='certification',
            name='report_issue_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
