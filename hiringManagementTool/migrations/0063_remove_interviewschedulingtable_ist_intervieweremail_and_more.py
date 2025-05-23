# Generated by Django 4.2.11 on 2025-03-31 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiringManagementTool', '0062_alter_interviewschedulingtable_ist_interviewstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interviewschedulingtable',
            name='ist_intervieweremail',
        ),
        migrations.RemoveField(
            model_name='interviewschedulingtable',
            name='ist_interviewername',
        ),
        migrations.RemoveField(
            model_name='interviewschedulingtable',
            name='ist_interviewtime',
        ),
        migrations.AddField(
            model_name='interviewschedulingtable',
            name='ist_interview_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interviewschedulingtable',
            name='ist_interview_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interviewschedulingtable',
            name='ist_interviewers',
            field=models.JSONField(blank=True, default=list, help_text="JSON array of objects, e.g., [{'name': 'John Doe', 'email': 'john.doe@example.com'}]"),
        ),
        migrations.AddField(
            model_name='interviewschedulingtable',
            name='ist_meeting_details',
            field=models.TextField(default='Not Provided', help_text='Stores physical address for ON_SITE, meeting link for VIDEO/GOOGLE_MEET/SKYPE, phone number for PHONE interviews.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='interviewschedulingtable',
            name='ist_createdate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='interviewschedulingtable',
            name='ist_interviewtype',
            field=models.PositiveSmallIntegerField(choices=[(1, 'VIDEO'), (2, 'ON_SITE'), (3, 'PHONE'), (4, 'GOOGLE_MEET'), (5, 'SKYPE'), (6, 'CODING_TEST')], default=1),
        ),
        migrations.AlterField(
            model_name='interviewschedulingtable',
            name='ist_updatedate',
            field=models.DateField(auto_now=True),
        ),
    ]
