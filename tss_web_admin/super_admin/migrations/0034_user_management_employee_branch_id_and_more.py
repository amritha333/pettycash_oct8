# Generated by Django 4.0.5 on 2022-08-31 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0033_alter_user_leave_draf_history_total_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_management',
            name='employee_branch_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user_management',
            name='employee_company_id',
            field=models.IntegerField(null=True),
        ),
    ]