# Generated by Django 4.0.5 on 2022-08-08 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0020_user_management_user_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_management',
            name='login_password_invalid_count',
            field=models.IntegerField(null=True),
        ),
    ]
