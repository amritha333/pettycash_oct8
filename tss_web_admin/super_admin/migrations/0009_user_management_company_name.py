# Generated by Django 4.0.5 on 2022-07-05 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0008_odoo_notification_auth_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_management',
            name='company_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
