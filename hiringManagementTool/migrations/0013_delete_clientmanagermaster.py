# Generated by Django 4.2.11 on 2025-02-18 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0012_remove_opendemand_dem_cmm_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClientManagerMaster',
        ),
    ]
