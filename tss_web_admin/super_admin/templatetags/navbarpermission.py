from ast import arg
from os import name, stat
from tkinter.messagebox import RETRY
from django import template
import json
register = template.Library()
from django.contrib.auth.models import User
from super_admin.models import *

from datetime import date


@register.filter(name='emp_url_perm_check')
def emp_url_perm_check(value,args):

   

    user_dat = User.objects.get(id=value)
    st = user_dat.is_superuser
   

    if st == True:
        return True
    else:
        

        today = date.today()
       
        permission_status = False
        try:
            data_user_role = user_role_mapping.objects.filter(auth_user_id=value,end_dt__gte=today,start_dt__lte=today) | user_role_mapping.objects.filter(auth_user_id=value,end_dt=None,start_dt__lte=today)
           
            
            role_id = list(data_user_role.values_list("role_id",flat=True))
            
            
           
            check_data = Role_permission_details.objects.filter(role_id__in=role_id,permission_name=args,read="on")

            
        

            if check_data:
                permission_status = True


        
        
            return permission_status
        except:
            return permission_status