
from ast import Try
from operator import mod
from pyexpat import model
from urllib import request
from django.db import models

from django.contrib.auth.models import User

# Create your models here.

from django.utils import timezone

from django.contrib.auth.models import User


# -----------------start   old database --------------
class User_details(models.Model):
    employee_id = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    department = models.CharField(max_length=255,null=True)
    branch = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255,null=True)



class User_leave_details(models.Model):
    user_id = models.ForeignKey(User_details,related_name="User_leave_details_user_id",on_delete=models.CASCADE,null=True)
    leave_type = models.CharField(max_length=255,null=True)
    from_dt = models.DateField(null=True)
    to_dt = models.DateField(null=True)
    total_days = models.IntegerField(null=True)
    available_leave = models.CharField(max_length=255,null=True)
    reason = models.TextField(null=True)
    attachment = models.FileField(upload_to="user_leave_attachment",null=True)
    annual_contact_no = models.CharField(max_length=255,null=True)
    name_of_replacer = models.CharField(max_length=255,null=True)
    tiket_entitled = models.CharField(max_length=255,null=True)
    destination = models.CharField(max_length=255,null=True)
    onward_journey = models.DateField(null=True)
    return_journey = models.DateField(null=True)
    family_entry = models.CharField(max_length=255,null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255,null=True)


# --------------end old database-------------------



# ----------new table --------------------



class Role_details(models.Model):
    auth_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    role_name = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255,null=True)


class Role_permission_details(models.Model):
    role_id = models.ForeignKey(Role_details,related_name="Role_permission_details_role_id",on_delete=models.CASCADE,null=True)
    permission_name = models.CharField(max_length=255,null=True)
    read = models.CharField(max_length=255,null=True)
    write = models.CharField(max_length=255,null=True)
    edit = models.CharField(max_length=255,null=True)
    delete = models.CharField(max_length=255,null=True)
    view_all = models.CharField(max_length=255,null=True)
    manage_all = models.CharField(max_length=255,null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255,null=True)
    



password_generate_option = (
    ("Automatic","Automatic"),
    ("Manual","Manual"),
)

password_expiration_status = (
    ("days","days"),
    ("none","none"),

)


class User_Management(models.Model):
    auth_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_management_user_login", null=True)
    username = models.CharField(max_length=255,null=True)
    password_option =  models.CharField(max_length=255,choices=password_generate_option,null=True)
    password = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    password_expiration_status = models.CharField(max_length=255,null=True,choices=password_expiration_status)
    password_expiration_total_days = models.IntegerField(null=True)
    password_expiration_end_date = models.DateField(null=True)
    effective_from_dt = models.DateField(null=True)
    effective_to_dt = models.DateField(null=True)
    employee_id = models.CharField(max_length=255,null=True)
    employee_branch = models.CharField(max_length=255,null=True)
    employee_department = models.CharField(max_length=255,null=True)
    employee_name = models.CharField(max_length=255,null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255,null=True)
    add_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_management_add_by_user_id", null=True)
    odoo_id = models.CharField(max_length=555,null=True)
    company_name = models.CharField(max_length=255,null=True)
    fcm_token=models.TextField(null=True) 
    user_img = models.TextField(null=True)
    login_password_invalid_count = models.IntegerField(null=True)
    employee_branch_id = models.IntegerField(null=True)
    employee_company_id = models.IntegerField(null=True)




class user_role_mapping(models.Model):
    auth_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_role_mapping_auth_user_login", null=True)
    user_id = models.ForeignKey(User_Management,on_delete=models.CASCADE,related_name="user_role_mapping_user_id",null=True)
    role_id = models.ForeignKey(Role_details,on_delete=models.CASCADE,null=True,related_name="user_role_mapping_role_id")
    start_dt = models.DateField(null=True)
    end_dt = models.DateField(null=True)
    description = models.TextField(null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=255,null=True)


class user_role_mapping_history(models.Model):
    user_role_mapping_id = models.ForeignKey(user_role_mapping,on_delete=models.CASCADE,related_name="user_role_mapping_history_mapping_id", null=True)
    start_dt = models.DateField(null=True)
    end_dt = models.DateField(null=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_role_mapping_history_updated_id", null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=255,null=True)



class odoo_api_request_token(models.Model):
    token = models.TextField(null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=255,null=True)


notification_type_data = (
    ("leave_type","leave_type"),
    ("leave_approve_request","leave_approve_request"),
   

)

notification_category_data = (
    ("notification","notification"),
    ("activities","activities")
)

class odoo_notification(models.Model):
    notification_type = models.CharField(max_length=255,null=True,choices=notification_type_data)
    message = models.TextField(null=True)
    mapping_id = models.IntegerField(null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    requested_from_dt = models.DateField(null=True)
    requested_to_dt = models.DateField(null=True)
    read_status = models.IntegerField(default=0)
    status = models.CharField(max_length=255,null=True)
    auth_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="odoo_notification_auth_user_login", null=True)
    leave_type_name = models.CharField(max_length=255,null=True)
    leave_approve_status = models.IntegerField(null=True)
    leave_apply_user_name = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    current_leave_status = models.CharField(max_length=255,null=True)
    category = models.CharField(max_length=255,null=True,choices=notification_category_data)




class test(models.Model):
    img_path = models.TextField()


class user_fcm_token(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fcm_token=models.TextField(null=True) 




class Leave_Status_details(models.Model):
    leave_mapping_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=255,null=True)
    dt = models.DateField(null=True)
    auth_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="leave_status_user_login", null=True)
    note = models.CharField(max_length=255,null=True)



class user_login_log_history(models.Model):
    auth_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_login_log_history_auth_user_login", null=True)
    user_id = models.ForeignKey(User_Management,on_delete=models.CASCADE,related_name="user_login_log_history_user_id",null=True)
    ip_address = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    lat_addre =  models.CharField(max_length=255,null=True)
    long_addr =  models.CharField(max_length=255,null=True)
    org = models.CharField(max_length=255,null=True)
    postal1 = models.CharField(max_length=255,null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=255,null=True)



class test_file_upload(models.Model):
    file_data = models.FileField(upload_to ='uploads/',null=True)




class pattern_lock_table(models.Model):
    auth_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="pattern_lock_user_login", null=True)
    pattern_number = models.TextField(null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=255,null=True)




class User_leave_draf_history(models.Model):
    auth_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User_leave_draf_history_user_login", null=True)
    user_id = models.ForeignKey(User_Management,on_delete=models.CASCADE,related_name="User_leave_draf_history_user_id",null=True)
    leave_type = models.CharField(max_length=255,null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    total_days = models.FloatField(null=True)
    reason = models.TextField(null=True)
    alternative_contact_number = models.CharField(max_length=255,null=True)
    employee_leave_replacer = models.IntegerField(null=True)
    holiday_type = models.CharField(max_length=255,null=True)
    employee_id = models.IntegerField(null=True)
    request_unit_half = models.CharField(max_length=255,null=True)
    request_date_form_period = models.CharField(max_length=255,null=True)
    absence_status = models.CharField(null=True,max_length=255)
    absence_category = models.CharField(max_length=255,null=True)
    attached_file = models.FileField(upload_to="leave_attached_file",null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=255,null=True)
    leave_type_id = models.IntegerField(null=True)
    employee_name = models.CharField(max_length=255,null=True)
    employee_reg_number = models.IntegerField(null=True)
    employee_replacer_name = models.CharField(max_length=255,null=True)
    

otp_type = (
    ("email_otp","email_otp"),
    ("sms_otp","sms_otp")
)


class Login_otp(models.Model):
    otp_type = models.CharField(max_length=255,null=True,choices=otp_type)
    email = models.CharField(max_length=255,null=True)
    otp = models.CharField(max_length=255,null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=255,null=True)
    auth_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Login_otp_user_login", null=True)





class User_company_details(models.Model):
    auth_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User_company_details_user_login", null=True)
    user_id = models.ForeignKey(User_Management,on_delete=models.CASCADE,related_name="User_company_details_user_id",null=True)
    company_name = models.CharField(max_length=255,null=True)
    company_id = models.IntegerField(null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    odoo_id = models.IntegerField(null=True)
    status = models.CharField(null=True,max_length=255)

class User_company_based_branch_details(models.Model):
    company_id = models.ForeignKey(User_company_details,on_delete=models.CASCADE,related_name="User_company_details_company_id")
    branch_name = models.CharField(null=True,max_length=255)
    branch_id = models.IntegerField(null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(null=True,max_length=255)