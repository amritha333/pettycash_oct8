# Generated by Django 4.0.5 on 2022-08-10 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0023_rename_postal_user_login_log_history_postal1'),
    ]

    operations = [
        migrations.CreateModel(
            name='test_file_upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_data', models.FileField(null=True, upload_to='uploads/')),
            ],
        ),
    ]
