from ast import arg
from posixpath import split
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
    print("new1111111111111 response1111::")
    print(response)
    data = []
    count = 0
    split_year_month = args.split("-")
    year = split_year_month[0]
    month = split_year_month[1]
    print("year:::",str(year))
    print("month:::",str(month))
    for i in response:
        print("iiii::::")
        print(i)
        col_before = 0
        colspan = 0
        if count == 0:
            from datetime import date
            import datetime
            lastDayOfMonth = datetime.date(int(year), int(month), 1)
            print("lastDayOfMonth:::::",str(lastDayOfMonth))
            for_loop_from_date = i['date_from']
            for_loop_from_date1 = datetime.datetime.fromisoformat(str(for_loop_from_date))
            for_loop_from_date12 = for_loop_from_date1.date()
            for_loop_from_year = str(for_loop_from_date12.year)
            for_loop_from_month = str(for_loop_from_date12.month)

            for_loop_to_date = i['date_to']
            for_loop_to_date1 = datetime.datetime.fromisoformat(str(for_loop_to_date))
            for_loop_to_date12 = for_loop_to_date1.date()
            for_loop_to_year = str(for_loop_to_date12.year)
            for_loop_to_month = str(for_loop_to_date12.month)
            import calendar
            import datetime

            days = calendar.monthrange(int(year), int(month))[1]
            print("total_days::::",str(days)) 

            last_date = datetime.date(int(year), int(month), days)
            print("last_date:::",str(last_date))

            if (year == for_loop_from_year and for_loop_from_month == month) and (for_loop_to_year == year and for_loop_to_month == month):
                print("---rrrssssssssssssss")
                df1 = datetime.datetime.fromisoformat(str(lastDayOfMonth))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days)
                print("c111ounttt:::::",str(delta.days))
                print("for_loop_to_date12::",str(for_loop_to_date12))
                print("for_loop_from_date12:::",str(for_loop_from_date12))
                col_span1 = for_loop_to_date12 - for_loop_from_date12
                colspan = int(col_span1.days)+1
                print("colspan::::",str(colspan))
            
            elif year == for_loop_from_year and for_loop_from_month == month:
                df1 = datetime.datetime.fromisoformat(str(lastDayOfMonth))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days)
                print("c111ounttt:::::",str(delta.days))
                col_span1 = last_date - for_loop_from_date12
                colspan = int(col_span1.days)+1
            elif for_loop_to_year == year and for_loop_to_month == month:
                df1 = datetime.datetime.fromisoformat(str(lastDayOfMonth))
                df11 = df1.date()
                delta = df11 - for_loop_from_date12 
                col_before = 0
                print("c111ounttt1111:::::",str(delta.days))
                col_span1 = for_loop_to_date12 - df11
                colspan = int(col_span1.days)+1
            else:
                print("rrrrrrrrrrrr11111111",str(count))
               
    
                days = calendar.monthrange(int(year), int(month))[1]
                print("total_days::::",str(days)) 
                col_before =0
                
                colspan = int(days)
                pass
                
        else:
            c1 = count  - 1
            previous_list = response[c1]
            print("previous_list11::::",str(count)+":::data:::",str(previous_list))
           
            previous_list_to_date = previous_list['date_to']
            print("previous_list_to_date:::",str(previous_list_to_date))
            from datetime import date
            import datetime
            previous_list_to_date1 = datetime.datetime.fromisoformat(str(previous_list_to_date))
            previous_list_to_date12 = previous_list_to_date1.date()
            previous_list_to_date_year = str(previous_list_to_date12.year)
            previous_list_to_date_month = str(previous_list_to_date12.month)

            for_loop_from_date = i['date_from']
            for_loop_from_date1 = datetime.datetime.fromisoformat(str(for_loop_from_date))
            for_loop_from_date12 = for_loop_from_date1.date()
            for_loop_from_year = str(for_loop_from_date12.year)
            for_loop_from_month = str(for_loop_from_date12.month)

            for_loop_to_date = i['date_to']
            for_loop_to_date1 = datetime.datetime.fromisoformat(str(for_loop_to_date))
            for_loop_to_date12 = for_loop_to_date1.date()
            for_loop_to_year = str(for_loop_to_date12.year)
            for_loop_to_month = str(for_loop_to_date12.month)
            import calendar
            import datetime

            days = calendar.monthrange(int(year), int(month))[1]
            print("total_days::::",str(days)) 

            last_date = datetime.date(int(year), int(month), days)
            print("last_date:::",str(last_date))

            if (previous_list_to_date_year == for_loop_from_year and for_loop_from_month == previous_list_to_date_month) and (for_loop_to_year == previous_list_to_date_year and for_loop_to_month == previous_list_to_date_month):
                print("---rrrssssssssssssss")
                df1 = datetime.datetime.fromisoformat(str(previous_list_to_date1))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days)-1
                print("c111ounttt:::::",str(delta.days))
                print("for_loop_to_date12::",str(for_loop_to_date12))
                print("for_loop_from_date12:::",str(for_loop_from_date12))
                col_span1 = for_loop_to_date12 - for_loop_from_date12
                colspan = int(col_span1.days)+1
                print("colspan::::",str(colspan))
            elif previous_list_to_date_year == for_loop_from_year and for_loop_from_month == previous_list_to_date_month:
                print("date1:::::",str(for_loop_from_date1)+":::count::",str(count))
                df1 = datetime.datetime.fromisoformat(str(previous_list_to_date1))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days) - 1
                print("c111ounttt:::::",str(delta.days))
                col_span1 = last_date - for_loop_from_date12
                colspan = int(col_span1.days)+1
            elif for_loop_to_year == previous_list_to_date_year and for_loop_to_month == previous_list_to_date_month:
                df1 = datetime.datetime.fromisoformat(str(previous_list_to_date1))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days)
                print("c111ounttt:::::",str(delta.days))
                col_span1 = for_loop_to_date12 - df11
                colspan = int(col_span1.days)+1
            else:
               
    
                days = calendar.monthrange(int(previous_list_to_date_year), int(previous_list_to_date_month))[1]
                print("total_days::::",str(days)) 
                col_before = int(days)
                
                colspan = int(days)
                pass
            print("countttt111:::::",str(count)+"::::data:::",str(col_before)+":::previous_list_to_date1::::",str(previous_list_to_date1))



            
            


            pass




           
            


        data.append({
            'id':i['id'],
            "holiday_status_id":i['holiday_status_id'],
            "date_from":i['date_from'],
            "date_to":i['date_to'],
            "number_of_days":i['number_of_days'],
            "col_before":col_before,
            "colspan":colspan

        })
        count = count + 1
        
        



    return data

    return response





@register.filter(name='get_user_leave_data1')
def get_user_leave_data1(value,args):
    print("value:::::",str(value))
    print("arg::::",str(args))
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    
    api_domain = "http://10.10.10.107:8069/"
    
    leave_history_response_url = api_domain+"api/get_leave_log_by_month"
    print("rs122223444444::::")

    print("odooo_id:::",str(value))
    print("arggg:::::",str(args))

    leave_history_payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id": int(value),
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
    print("r1222222223334444555556666::")
    print(response)
    data = []
    count = 0
    split_year_month = args.split("-")
    year = split_year_month[0]
    month = split_year_month[1]
    print("year:::",str(year))
    print("month:::",str(month))
    for i in response:
        print("iiii::::")
        print(i)
        col_before = 0
        colspan = 0
        if count == 0:
            from datetime import date
            import datetime
            lastDayOfMonth = datetime.date(int(year), int(month), 1)
            print("lastDayOfMonth:::::",str(lastDayOfMonth))
            for_loop_from_date = i['date_from']
            for_loop_from_date1 = datetime.datetime.fromisoformat(str(for_loop_from_date))
            for_loop_from_date12 = for_loop_from_date1.date()
            for_loop_from_year = str(for_loop_from_date12.year)
            for_loop_from_month = str(for_loop_from_date12.month)

            for_loop_to_date = i['date_to']
            for_loop_to_date1 = datetime.datetime.fromisoformat(str(for_loop_to_date))
            for_loop_to_date12 = for_loop_to_date1.date()
            for_loop_to_year = str(for_loop_to_date12.year)
            for_loop_to_month = str(for_loop_to_date12.month)
            import calendar
            import datetime

            days = calendar.monthrange(int(year), int(month))[1]
            print("total_days::::",str(days)) 

            last_date = datetime.date(int(year), int(month), days)
            print("last_date:::",str(last_date))

            if (year == for_loop_from_year and for_loop_from_month == month) and (for_loop_to_year == year and for_loop_to_month == month):
                print("---rrrssssssssssssss")
                df1 = datetime.datetime.fromisoformat(str(lastDayOfMonth))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days)
                print("c111ounttt:::::",str(delta.days))
                print("for_loop_to_date12::",str(for_loop_to_date12))
                print("for_loop_from_date12:::",str(for_loop_from_date12))
                col_span1 = for_loop_to_date12 - for_loop_from_date12
                colspan = int(col_span1.days)+1
                print("colspan::::",str(colspan))
            
            elif year == for_loop_from_year and for_loop_from_month == month:
                df1 = datetime.datetime.fromisoformat(str(lastDayOfMonth))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days)
                print("c111ounttt:::::",str(delta.days))
                col_span1 = last_date - for_loop_from_date12
                colspan = int(col_span1.days)+1
            elif for_loop_to_year == year and for_loop_to_month == month:
                df1 = datetime.datetime.fromisoformat(str(lastDayOfMonth))
                df11 = df1.date()
                delta = df11 - for_loop_from_date12 
                col_before = 0
                print("c111ounttt1111:::::",str(delta.days))
                col_span1 = for_loop_to_date12 - df11
                colspan = int(col_span1.days)+1
            else:
                print("rrrrrrrrrrrr11111111",str(count))
               
    
                days = calendar.monthrange(int(year), int(month))[1]
                print("total_days::::",str(days)) 
                col_before =0
                
                colspan = int(days)
                pass
                
        else:
            c1 = count  - 1
            previous_list = response[c1]
            print("previous_list11::::",str(count)+":::data:::",str(previous_list))
           
            previous_list_to_date = previous_list['date_to']
            print("previous_list_to_date:::",str(previous_list_to_date))
            from datetime import date
            import datetime
            previous_list_to_date1 = datetime.datetime.fromisoformat(str(previous_list_to_date))
            previous_list_to_date12 = previous_list_to_date1.date()
            previous_list_to_date_year = str(previous_list_to_date12.year)
            previous_list_to_date_month = str(previous_list_to_date12.month)

            for_loop_from_date = i['date_from']
            for_loop_from_date1 = datetime.datetime.fromisoformat(str(for_loop_from_date))
            for_loop_from_date12 = for_loop_from_date1.date()
            for_loop_from_year = str(for_loop_from_date12.year)
            for_loop_from_month = str(for_loop_from_date12.month)

            for_loop_to_date = i['date_to']
            for_loop_to_date1 = datetime.datetime.fromisoformat(str(for_loop_to_date))
            for_loop_to_date12 = for_loop_to_date1.date()
            for_loop_to_year = str(for_loop_to_date12.year)
            for_loop_to_month = str(for_loop_to_date12.month)
            import calendar
            import datetime

            days = calendar.monthrange(int(year), int(month))[1]
            print("total_days::::",str(days)) 

            last_date = datetime.date(int(year), int(month), days)
            print("last_date:::",str(last_date))

            if (previous_list_to_date_year == for_loop_from_year and for_loop_from_month == previous_list_to_date_month) and (for_loop_to_year == previous_list_to_date_year and for_loop_to_month == previous_list_to_date_month):
                print("---rrrssssssssssssss")
                df1 = datetime.datetime.fromisoformat(str(previous_list_to_date1))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days)-1
                print("c111ounttt:::::",str(delta.days))
                print("for_loop_to_date12::",str(for_loop_to_date12))
                print("for_loop_from_date12:::",str(for_loop_from_date12))
                col_span1 = for_loop_to_date12 - for_loop_from_date12
                colspan = int(col_span1.days)+1
                print("colspan::::",str(colspan))
            elif previous_list_to_date_year == for_loop_from_year and for_loop_from_month == previous_list_to_date_month:
                print("date1:::::",str(for_loop_from_date1)+":::count::",str(count))
                df1 = datetime.datetime.fromisoformat(str(previous_list_to_date1))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days) - 1
                print("c111ounttt:::::",str(delta.days))
                col_span1 = last_date - for_loop_from_date12
                colspan = int(col_span1.days)+1
            elif for_loop_to_year == previous_list_to_date_year and for_loop_to_month == previous_list_to_date_month:
                df1 = datetime.datetime.fromisoformat(str(previous_list_to_date1))
                df11 = df1.date()
                delta = for_loop_from_date12 - df11
                col_before = int(delta.days)
                print("c111ounttt:::::",str(delta.days))
                col_span1 = for_loop_to_date12 - df11
                colspan = int(col_span1.days)+1
            else:
               
    
                days = calendar.monthrange(int(previous_list_to_date_year), int(previous_list_to_date_month))[1]
                print("total_days::::",str(days)) 
                col_before = int(days)
                
                colspan = int(days)
                pass
            print("countttt111:::::",str(count)+"::::data:::",str(col_before)+":::previous_list_to_date1::::",str(previous_list_to_date1))



            
            


            pass




           
            

        
        data.append({
            'id':i['id'],
            "holiday_status_id":i['holiday_status_id'],
            "date_from":i['date_from'],
            "date_to":i['date_to'],
            "number_of_days":i['number_of_days'],
            "col_before":col_before,
            "colspan":colspan

        })
        count = count + 1
        
        



    return data

    return response





@register.filter(name='check_month_differnce')
def check_month_differnce(value,args):
    print("values::::::",str(value))
    print("args::::",str(args))
    print("type:::::",type(args))
    import datetime
    aDateTime = datetime.datetime.fromisoformat(str(args))
    print("convert date11::::",str(aDateTime.date()))

    split_year_month = value.split("-")
    year = split_year_month[0]
    month = split_year_month[1]
    print("year:::",str(year))
    print("month:::",str(month))
    from datetime import date

    
    lastDayOfMonth = datetime.date(int(year), int(month), 1)
    print("lastDayOfMonth:::::",str(lastDayOfMonth))



    return True
    pass