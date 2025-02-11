# Generated by Django 4.2.11 on 2025-02-11 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0005_alter_candidatemaster_cdm_csm_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internaldepartmentmaster',
            name='idm_spoc_id',
            field=models.ForeignKey(blank=True, db_column='idm_spoc_id', help_text='Single Point of Contact (SPOC) from Employee Master', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_master', to='hiringManagementTool.employeemaster'),
        ),
    ]
