# Generated by Django 4.0.5 on 2022-09-20 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0039_alter_petty_cash_expense_draft_history_expense_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='odoo_notification',
            name='expense_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]