# Generated by Django 4.2.11 on 2025-03-04 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0029_alter_candidatedemandlink_cdl_joiningdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='opendemand',
            old_name='position_name',
            new_name='dem_position_name',
        ),
    ]
