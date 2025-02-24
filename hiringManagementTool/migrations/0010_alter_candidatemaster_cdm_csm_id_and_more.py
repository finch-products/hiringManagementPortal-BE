# Generated by Django 4.2.11 on 2025-02-12 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0009_alter_internaldepartmentmaster_idm_deliverymanager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatemaster',
            name='cdm_csm_id',
            field=models.ForeignKey(blank=True, db_column='cdm_csm_id', help_text='Reference to another candidate (if applicable)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='candidate_references', to='hiringManagementTool.candidatestatusmaster'),
        ),
        migrations.AlterField(
            model_name='clientmanagermaster',
            name='cmm_clm_id',
            field=models.ForeignKey(db_column='cmm_clm_id', help_text='Foreign Key from ClientMaster table', on_delete=django.db.models.deletion.CASCADE, related_name='client_managers', to='hiringManagementTool.clientmaster'),
        ),
        migrations.AlterField(
            model_name='clientmaster',
            name='clm_lcm_id',
            field=models.ForeignKey(db_column='clm_lcm_id', help_text='Reference to Location Master Table', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_client', to='hiringManagementTool.locationmaster'),
        ),
        migrations.AlterField(
            model_name='employeemaster',
            name='emp_lcm_id',
            field=models.ForeignKey(db_column='emp_lcm_id', help_text='Reference to Location Master Table', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_employee', to='hiringManagementTool.locationmaster'),
        ),
        migrations.AlterField(
            model_name='employeemaster',
            name='emp_rlm_id',
            field=models.ForeignKey(blank=True, db_column='emp_rlm_id', help_text='Role ID associated with the employee', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_employee', to='hiringManagementTool.rolemaster'),
        ),
        migrations.AlterField(
            model_name='opendemand',
            name='dem_clm_id',
            field=models.ForeignKey(db_column='dem_clm_id', help_text='Reference to Client Master Table', on_delete=django.db.models.deletion.CASCADE, related_name='client_demands', to='hiringManagementTool.clientmaster'),
        ),
        migrations.AlterField(
            model_name='opendemand',
            name='dem_cmm_id',
            field=models.ForeignKey(db_column='dem_cmm_id', help_text='Reference to Client Manager', on_delete=django.db.models.deletion.CASCADE, related_name='demands', to='hiringManagementTool.clientmanagermaster'),
        ),
        migrations.AlterField(
            model_name='opendemand',
            name='dem_dsm_id',
            field=models.ForeignKey(db_column='dem_dsm_id', help_text='Reference to Internal Department Master Table', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dsm_demands', to='hiringManagementTool.demandstatusmaster'),
        ),
        migrations.AlterField(
            model_name='opendemand',
            name='dem_idm_id',
            field=models.ForeignKey(db_column='dem_idm_id', help_text='Reference to Internal Department Master Table', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idm_demands', to='hiringManagementTool.internaldepartmentmaster'),
        ),
        migrations.AlterField(
            model_name='opendemand',
            name='dem_lcm_id',
            field=models.ForeignKey(db_column='dem_lcm_id', help_text='Reference to Location Master Table', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_demands', to='hiringManagementTool.locationmaster'),
        ),
        migrations.AlterField(
            model_name='opendemand',
            name='dem_lob_id',
            field=models.ForeignKey(db_column='dem_lob_id', help_text='Reference to LOB Master Table', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lob_demands', to='hiringManagementTool.lobmaster'),
        ),
    ]
