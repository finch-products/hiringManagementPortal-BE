# Generated by Django 5.1.5 on 2025-02-21 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0021_rename_dsm_insertby_demandstatusmaster_dsm_insertby_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='opendemand',
            name='position_name',
            field=models.TextField(blank=True, help_text='Name of the position', null=True),
        )
    ]
