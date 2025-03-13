# Generated by Django 5.1.5 on 2025-03-13 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0043_candidatestatusmaster_dsm_inactive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidatestatusmaster',
            name='dsm_inactive',
        ),
        migrations.AddField(
            model_name='candidatestatusmaster',
            name='csm_inactive',
            field=models.BooleanField(db_column='csm_inactive', default=False, help_text='If True (1), this status will not be listed in the application'),
        ),
    ]
