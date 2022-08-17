# Generated by Django 4.0.5 on 2022-08-17 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0030_user_leave_draf_history_employee_replacer_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login_otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_type', models.CharField(choices=[('email_otp', 'email_otp'), ('sms_otp', 'sms_otp')], max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('otp', models.CharField(max_length=255, null=True)),
                ('dt', models.DateField(auto_now_add=True)),
                ('tm', models.TimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
