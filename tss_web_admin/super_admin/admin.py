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