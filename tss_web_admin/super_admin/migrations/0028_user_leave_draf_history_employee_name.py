# Generated by Django 4.0.5 on 2022-08-13 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0027_user_leave_draf_history_leave_type_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_leave_draf_history',
            name='employee_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
