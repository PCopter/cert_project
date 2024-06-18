# Generated by Django 5.0.4 on 2024-05-03 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=60)),
                ('indoor_model_name', models.CharField(max_length=60)),
                ('outdoor_model_name', models.CharField(max_length=60)),
                ('remark', models.CharField(max_length=60, null=True)),
                ('report_no', models.CharField(max_length=60, null=True)),
                ('report_issue_date', models.DateTimeField(null=True)),
            ],
        ),
    ]