# Generated by Django 4.2.1 on 2023-05-27 15:21

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_account_evidence_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='evidence',
            field=models.FileField(blank=True, null=True, upload_to=core.models.Report.report_document_loc),
        ),
    ]