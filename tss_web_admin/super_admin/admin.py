from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User_details)
admin.site.register(User_leave_details)
admin.site.register(Role_details)
admin.site.register(Role_permission_details)
admin.site.register(User_Management)
admin.site.register(user_role_mapping)
admin.site.register(user_role_mapping_history)
admin.site.register(odoo_api_request_token)
admin.site.register(odoo_notification)
admin.site.register(test)
admin.site.register(user_fcm_token)
admin.site.register(Leave_Status_details)
admin.site.register(user_login_log_history)
admin.site.register(test_file_upload)
admin.site.register(User_leave_draf_history)
admin.site.register(Login_otp)
admin.site.register(User_company_details)
admin.site.register(User_company_based_branch_details)
admin.site.register(petty_cash_draft_history)
admin.site.register(petty_cash_expense_draft_history)
admin.site.register(petty_cash_attachments)