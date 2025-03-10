# Generated by Django 4.2.11 on 2025-02-09 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0002_alter_employeemaster_emp_updateby'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StrategicBusinessUnitMaster',
        ),
        migrations.RenameField(
            model_name='candidatedemandhistory',
            old_name='cdh_cdm',
            new_name='cdh_cdm_id',
        ),
        migrations.RenameField(
            model_name='candidatemaster',
            old_name='cdm_csm',
            new_name='cdm_csm_id',
        ),
        migrations.RenameField(
            model_name='candidatemaster',
            old_name='cdm_empid',
            new_name='cdm_emp_id',
        ),
        migrations.RenameField(
            model_name='candidatestatusmaster',
            old_name='csm_sortId',
            new_name='csm_sortid',
        ),
        migrations.RenameField(
            model_name='demandhistorytable',
            old_name='dhs_dsm_sortId',
            new_name='dhs_dsm_sortid',
        ),
        migrations.RenameField(
            model_name='demandstatusmaster',
            old_name='dsm_sortId',
            new_name='dsm_sortid',
        ),
        migrations.RenameField(
            model_name='opendemand',
            old_name='dem_clm',
            new_name='dem_clm_id',
        ),
        migrations.RenameField(
            model_name='opendemand',
            old_name='dem_cmm',
            new_name='dem_cmm_id',
        ),
        migrations.RenameField(
            model_name='opendemand',
            old_name='dem_lcm',
            new_name='dem_lcm_id',
        ),
        migrations.AlterField(
            model_name='employeemaster',
            name='emp_updateby',
            field=models.IntegerField(blank=True, help_text='User ID who updated the record', null=True),
        ),
        migrations.AlterField(
            model_name='opendemand',
            name='dem_dsm_id',
            field=models.ForeignKey(help_text='Reference to Internal Department Master Table', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dsm_demands', to='hiringManagementTool.demandstatusmaster'),
        ),
        migrations.AlterField(
            model_name='opendemand',
            name='dem_idm_id',
            field=models.ForeignKey(help_text='Reference to Internal Department Master Table', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idm_demands', to='hiringManagementTool.internaldepartmentmaster'),
        ),
    ]
