# Generated by Django 4.2.11 on 2025-03-19 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0050_remove_opendemand_dem_position_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='opendemand',
            name='dem_position_location',
            field=models.CharField(blank=True, help_text='Position Location', max_length=100, null=True),
        ),
    ]
