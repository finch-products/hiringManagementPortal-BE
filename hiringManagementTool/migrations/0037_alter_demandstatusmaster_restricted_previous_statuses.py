# Generated by Django 5.1.5 on 2025-03-12 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0036_demandstatusmaster_restricted_previous_statuses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandstatusmaster',
            name='restricted_previous_statuses',
            field=models.ManyToManyField(blank=True, db_column='restricted_previous_statuses', help_text='List of statuses that are NOT allowed to transition to this status', related_name='restricted_next_statuses', to='hiringManagementTool.demandstatusmaster'),
        ),
    ]
