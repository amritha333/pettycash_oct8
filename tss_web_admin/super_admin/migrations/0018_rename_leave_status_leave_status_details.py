# Generated by Django 4.0.5 on 2022-07-26 05:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('super_admin', '0017_leave_status_auth_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='leave_status',
            new_name='Leave_Status_details',
        ),
    ]