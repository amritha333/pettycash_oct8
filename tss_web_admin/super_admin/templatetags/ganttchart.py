from ast import arg
from django import template

register = template.Library()
import requests
from super_admin.models import *
import json
@register.filter(name='get_leave_available')
def get_leave_available(value,args):
    print("value:::::",str(value))
    print("arg::::",str(args))

    user_data = User_Management.objects.get(auth_user=value)
    print("user_data:::",str(user_data.odoo_id))
    response = ""
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    
    api_domain = "http://10.10.10.107:8069/"
    
    leave_history_response_url = api_domain+"api/get_leave_of_a_day"
    print("rs122223444444::::")

    print("odooo_id:::",str(user_data.odoo_id))
    print("arggg:::::",str(args))

    leave_history_payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id": int(user_data.odoo_id),
            "start_date" : str(args)
        }
    })
    
    leave_history_headers = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    print("rs122223444444::::")

    leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers, data=leave_history_payload).json()
    print("rs122223::::")
        
    leave_history_response12  = leave_history_response1['result']
    response = leave_history_response12['result']
    print("r1::")
    print(response)
    response1 = False

    if response:
        response1 = True
    

        

  


    print("endddd-----------------")


    return response




@register.filter(name='get_leave_available1')
def get_leave_available1(value,args):
    print("value:::::",str(value))
    print("arg::::",str(args))

    
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    
    api_domain = "http://10.10.10.107:8069/"
    
    leave_history_response_url = api_domain+"api/get_leave_of_a_day"
    print("rs122223444444::::")

    print("odooo_id:::",str(value))
    print("arggg:::::",str(args))

    leave_history_payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id": int(value),
            "start_date" : str(args)
        }
    })
    
    leave_history_headers = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    print("rs122223444444::::")

    leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers, data=leave_history_payload).json()
    print("rs122223::::")
        
    leave_history_response12  = leave_history_response1['result']
    response = leave_history_response12['result']
    print("r1::")
    print(response)
    response1 = False

    if response:
        response1 = True
    

        

  


    print("endddd-----------------")


    return response





@register.filter(name='get_user_leave_data')
def get_user_leave_data(value,args):
    print("value:::::",str(value))
    print("arg::::",str(args))
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    user_data = User_Management.objects.get(auth_user=value)
    api_domain = "http://10.10.10.107:8069/"
    
    leave_history_response_url = api_domain+"api/get_leave_log_by_month"
    print("rs122223444444::::")

    print("odooo_id:::",str(value))
    print("arggg:::::",str(args))

    leave_history_payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id": int(user_data.odoo_id),
            "date" : args
        }
    })
    
    leave_history_headers = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    print("rs122223444444::::")

    leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers, data=leave_history_payload).json()
    print("rs122223::::")
        
    leave_history_response12  = leave_history_response1['result']
    response = leave_history_response12['result']
    print("r122222222333444455555::")
    print(response)

    return response