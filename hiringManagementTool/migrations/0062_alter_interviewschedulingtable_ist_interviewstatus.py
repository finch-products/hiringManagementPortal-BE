# Generated by Django 4.2.11 on 2025-03-28 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0061_merge_20250328_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewschedulingtable',
            name='ist_interviewstatus',
            field=models.PositiveSmallIntegerField(choices=[(1, 'SCHEDULED'), (2, 'RESCHEDULED'), (3, 'COMPLETED'), (4, 'CANCELLED')], default=1),
        ),
    ]
