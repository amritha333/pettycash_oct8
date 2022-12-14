# Generated by Django 4.0.5 on 2022-09-01 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('super_admin', '0034_user_management_employee_branch_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_company_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('company_id', models.IntegerField(null=True)),
                ('dt', models.DateField(auto_now_add=True)),
                ('tm', models.TimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('auth_user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_company_details_user_login', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_company_details_user_id', to='super_admin.user_management')),
            ],
        ),
        migrations.CreateModel(
            name='User_company_based_branch_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=255, null=True)),
                ('branch_id', models.IntegerField(null=True)),
                ('dt', models.DateField(auto_now_add=True)),
                ('tm', models.TimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_company_details_company_id', to='super_admin.user_company_details')),
            ],
        ),
    ]
