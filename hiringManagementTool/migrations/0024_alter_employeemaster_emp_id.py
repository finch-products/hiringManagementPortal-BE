# Generated by Django 4.2.11 on 2025-02-24 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0023_remove_demandhistory_dhs_insertby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opendemand',
            name='dem_id',
            field=models.CharField(editable=False, help_text='Auto-generated ID in format emp_ddmmyyyy_1', max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='employeemaster',
            name='emp_id',
            field=models.CharField(editable=False, help_text='Auto-generated ID in format emp_ddmmyyyy_1', max_length=50, primary_key=True, serialize=False),
        ),
    ]
