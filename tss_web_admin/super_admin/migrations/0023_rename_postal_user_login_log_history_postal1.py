# Generated by Django 4.0.5 on 2022-08-08 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0022_user_login_log_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_login_log_history',
            old_name='postal',
            new_name='postal1',
        ),
    ]