# Generated by Django 4.0.5 on 2022-10-06 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0042_alter_petty_cash_expense_draft_history_job_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='odoo_notification',
            name='company_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='odoo_notification',
            name='employee_branch',
            field=models.CharField(max_length=255, null=True),
        ),
    ]