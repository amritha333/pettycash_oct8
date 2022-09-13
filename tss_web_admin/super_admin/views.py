from lib2to3.pgen2 import token
import mailbox
from math import fabs
from multiprocessing import context
from os import stat
from turtle import st
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer

from .decorators import *





def inside_user_permission(permission_name,user_id):
    today = date.today()
    user_dat = User.objects.get(id=user_id.id)
    user_role = user_dat.is_superuser
    if user_role == True:
        data = {
                'view_all':True,
                'read':True,
                'write':True,
                'edit':True,
                'delete':True
        }
        return data

    user_role_mapping_instance = user_role_mapping.objects.filter(auth_user_id=user_id,end_dt__gte=today,start_dt__lte=today) | user_role_mapping.objects.filter(auth_user_id=user_id,end_dt=None,start_dt__lte=today)
    role_id = list(user_role_mapping_instance.values_list("role_id",flat=True))
    check_instance = Role_permission_details.objects.filter(role_id__in=role_id,permission_name=permission_name)
    if check_instance:
        if check_instance.filter(manage_all="on"):
            data = {
                'view_all':True,
                'read':True,
                'write':True,
                'edit':True,
                'delete':True
            }
            return data
        elif check_instance.filter(view_all="on"):

            write = False
            if check_instance.filter(write="on"):
                write = True
            edit = False
            if check_instance.filter(edit="on"):
                edit = True
            
            delete = False

            if check_instance.filter(delete="on"):
                delete = True



            data = {
                'view_all':True,
                'read':True,
                'write':write,
                'edit':edit,
                'delete':delete
            }
            return data
            
        elif check_instance.filter(read="on"):
            write = False
            if check_instance.filter(write="on"):
                write = True
            edit = False
            if check_instance.filter(edit="on"):
                edit = True
            
            delete = False

            if check_instance.filter(delete="on"):
                delete = True



            data = {
                'view_all':False,
                'read':True,
                'write':write,
                'edit':edit,
                'delete':delete
            }
            return data

       
    else:
        pass





    pass




def index(request):
    user_email = ""
    try:

        user_email = request.session['user_email']
    except:
        pass

    return render(request,'super_admin/index.html',{'user_email':user_email})



def login_page1(request):
    return render(request,'super_admin/logout.html')





api_domain = "http://10.10.10.126:8069/"



@login_required(login_url='/index')
def admin_dashboard(request):
    user = request.user

    try:
        data = pattern_lock_table.objects.get(auth_user_id=request.user,status='True')
        return render(request,'super_admin/pattern_lock.html')
        
    except:
        pass
    
    user_dat = User.objects.get(id=request.user.id)
    st = user_dat.is_superuser
 

    total_user_count = User_details.objects.all().count()
    total_active_user = User_details.objects.filter(status="True").count()
    total_inactive_user = User_details.objects.filter(status="False").count()
    user_data = User_details.objects.all().order_by("-id")[1:5]

    context = {
        'total_user_count':total_user_count,
        'total_active_user':total_active_user,
        'total_inactive_user':total_inactive_user,
        'user_data':user_data,
        'room_name': "broadcast2",
    }
    return render(request,'super_admin/admin_home.html',context)



def user_home(request):
    user_login_id = request.session['user_login_id']
    
    return render(request,'super_admin/user_home.html')
import json
import aiohttp
import asyncio



async def odoo_test_login_api(request):
    token_url = api_domain+"api/get_api_key"
    payload = json.dumps({ "jsonrpc": "2.0","params": {"login": "admin","password": "admin","db": "tss-latest"}})
    headers = {'Content-Type': 'application/json','Cookie': 'session_id=9d67dcc82ed899ef3c1b3bbe0b6377464c46a52d'}
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url, headers=headers, data=payload) as res:
            response1 = await res.json()
            response12 =response1['result']
            return response12

    pass

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_action(request):

    if request.method == "POST":
        from datetime import date
        uname = request.POST.get("uname",False)
        passwrd = request.POST.get("passwrd",False)
        country = request.POST.get("country",False)
        state = request.POST.get("state",False)
        city = request.POST.get("city",False)
        latitude = request.POST.get("latitude",False)
        longitude = request.POST.get("longitude",False)
        ipv4 = request.POST.get("ipv4",False)

        data =[]
        data = {
            'message':'success'
        }
        
        if User.objects.filter(username=uname).exists():
            
            user = authenticate(username=uname, password=passwrd)
            if user == None:
                user_data = User.objects.get(username=uname)
                try:
                    user_management = User_Management.objects.get(auth_user=user_data)
                    prv_count = user_management.login_password_invalid_count
                    if prv_count == None:
                        prv_count = 0
                    count = prv_count + 1 
                    print("count:::::",str(count))
                    if count > 3:
                        update_password_count = User_Management.objects.filter(auth_user=user_data).update(login_password_invalid_count=count,status=False)
                        context={
                                'message':"userblocked"
                                
                        }  
                        return JsonResponse(context,safe=False) 
                        return render(request,'super_admin/index.html',context)
                    else:
                        update_password_count = User_Management.objects.filter(auth_user=user_data).update(login_password_invalid_count=count)

                    
                except:
                    pass
            
        user = authenticate(username=uname, password=passwrd)
        remember = request.POST.get("remember",False)
        if user is not None:
            if remember == "yes":
                request.session['user_email'] = uname
            else:
                request.session['user_email'] = ""
            st = user.is_superuser
            try:
                alredy_exists_odoo_token = odoo_api_request_token.objects.get(status="True")
                # if alredy_exists_odoo_token is not None:
                #     update_token =  odoo_api_request_token.objects.filter(status="True").update(
                #         token = json_response['result']
                #     )
            except odoo_api_request_token.DoesNotExist:
                get_response = asyncio.run(odoo_test_login_api(request))
                json_response = get_response
                save_token = odoo_api_request_token(
                    token = json_response['result'],
                    status = "True" 
                )
                save_token.save()
            # login(request, user)
            try:
                data_email_otp = Login_otp.objects.get(auth_user_id_id= user.id)
                context={
                        'message':"email_otp",
                            
                }
                return JsonResponse(context,safe=False) 
            except Login_otp.DoesNotExist:
                pass
            if st == True:
                context={
                        'message':"success",
                            
                }
                print("successss")
                return JsonResponse(context,safe=False) 
                
                return redirect("admin_dashboard")
            elif st == False:
               
                user_management = User_Management.objects.get(auth_user=user)
                print("heyyyyyyyyyyyyyy")
                user_login_log = user_login_log_history.objects.create(
                    auth_user_id = user,
                    user_id_id = user_management.id,
                    ip_address =str(ipv4),
                    address = str(state),
                    city = str(city),
                    country = str(country),
                    lat_addre = str(latitude),
                    long_addr = str(longitude),
                    
                    status = "True"


                )

                today = date.today()
                try:
                    login_effective = User_Management.objects.filter(auth_user=user,effective_to_dt__gte=today,effective_from_dt__lte=today,status=True) | User_Management.objects.filter(auth_user=user,effective_from_dt__lte=today,effective_to_dt=None,status=True)
                    
                    if login_effective:
                        update_password_count = User_Management.objects.filter(auth_user=user).update(login_password_invalid_count=0,status=True)
                        context={
                            'message':"success",
                            
                        }
                        print("successss")
                        return JsonResponse(context,safe=False) 
                        return redirect("admin_dashboard")
                    else:
                        try:
                            date_data = User_Management.objects.get(auth_user=user,status=False)
                            print("blockedddddddddd")
                            context={
                                'message':"userblocked"
                                
                            }   
                            return JsonResponse(context,safe=False) 
                        except:
                            
                            date_data = User_Management.objects.get(auth_user=user)
                            login_date = date_data.effective_from_dt
                            context={
                                'message':"login_date_error",
                                'login_date':login_date
                            }
                            return JsonResponse(context,safe=False) 
                            return render(request,'super_admin/index.html',context)

                except User_Management.DoesNotExist:
                    date_data = User_Management.objects.get(auth_user=user)
                    login_date = date_data.effective_from_dt
                    context={
                        'message':"login_date_error",
                        'login_date':login_date
                    }
                    return JsonResponse(context,safe=False) 
                    return render(request,'super_admin/index.html',context)
                    pass
                
                
                print("employeeee___")
                pass
        else:
            try:
                user_login = User_details.objects.get(username=uname,password=passwrd,status="True")
                request.session['user_login_id'] = user_login.id
                return redirect("user_home")
            except User_details.DoesNotExist:
                context = {}
                context['message'] = "error"
                return JsonResponse(context,safe=False) 
                return render(request,'super_admin/index.html',context)



@login_required(login_url='/index')
def admin_add_user(request):

    return render(request,'super_admin/admin_add_user.html')


@login_required(login_url='/index')
def menu(request):
    return render(request,'super_admin/menu.html')



from rest_framework.decorators import api_view
from .seralizer import User_detailsSerializer

@api_view(['POST'])
def admin_add_user_action(request):
    


    username = request.POST.get("username")
   

    try:
        username_exists = User_details.objects.get(username=username)
        return render(request,'super_admin/admin_add_user.html',{"message":"username alredy exists"})
    except User_details.DoesNotExist:
        pass
    
    employee_id = request.POST.get("employee_id")
    try:
        employee_id_exists = User_details.objects.get(employee_id=employee_id)
        return render(request,'super_admin/admin_add_user.html',{"message":"employee id alredy exists"})
    except User_details.DoesNotExist:
        pass


    
    serializer = User_detailsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()

        
        S = 10  # number of characters in the string.  
        import string    
        import random

        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        update_password = User_details.objects.filter(id=instance.id).update(password=password,status="True")
        
        return render(request,'super_admin/admin_add_user.html',{'message':'added'})
        pass

    pass



@login_required(login_url='/index')
def admin_view_user(request):

    data = User_details.objects.all()
    context = {
        'data':data
    }
    return render(request,'super_admin/admin_view_user.html',context)



@login_required(login_url='/index')
def admin_delete_user_action(request):
    if request.method == "POST":
        id = request.POST.get("id")
        
        data_delte = User_details.objects.get(id=id).delete()
        return redirect("admin_view_user")



@login_required(login_url='/index')
def admin_edit_user_details_action(request):

    if request.method == "POST":
        employee_id = request.POST.get("employee_id",False)
        id1 = request.POST.get("id1",False)
        name = request.POST.get("name",False)
        department = request.POST.get("department",False)
        branch = request.POST.get("branch",False)
        username = request.POST.get("username",False)
        password = request.POST.get("password",False)
        data_updated = User_details.objects.filter(id=id1).update(employee_id=employee_id,
        name=name,
        department=department,
        branch=branch,
        username=username,
        password=password
        
        
        )
        data = User_details.objects.all()
        context = {
            'data':data,
            'message':'updated'
        }
        return render(request,'super_admin/admin_view_user.html',context)



@login_required(login_url='/index')
def admin_inactive_user_action(request):
    if request.method == "POST":
        id2 = request.POST.get("id2",False)
        data_inactive = User_details.objects.filter(id=id2).update(status="False")
        data = User_details.objects.all()
        context = {
            'data':data,
            'message':'inactive'
        }
        return render(request,'super_admin/admin_view_user.html',context)


@login_required(login_url='/index')
def admin_active_user_action(request):
    if request.method == "POST":
        id2 = request.POST.get("id3",False)
        data_inactive = User_details.objects.filter(id=id2).update(status="True")
        data = User_details.objects.all()
        context = {
            'data':data,
            'message':'active'
        }
        return render(request,'super_admin/admin_view_user.html',context)

        

def user_apply_leave_management(request):
    user_login_id = request.session['user_login_id']

   




    return render(request,'super_admin/user_apply_leave_management.html')



def user_apply_leave_action(request):
    if request.method == "POST":

        # file = request.FILES['pic']
        # print("fileeeeeeeeeeeeeeeeeeeeeeeee")
        # print(file)

        # return

        

        user_data = User_Management.objects.get(auth_user_id=request.user.id)
        user_login_id = user_data.id
        leave_type = request.POST.get("leave_type",False)
        from_dt = request.POST.get("from_dt",False)
        to_dt = request.POST.get("to_dt",False)
        total_days = request.POST.get("total_days",False)
        available_leave = request.POST.get("available_leave",False)
        reason = request.POST.get("reason",False)
        
        annual_contact_no = request.POST.get("annual_contact_no",False)
        name_of_replacer = request.POST.get("name_of_replacer",False)
        tiket_entitled = request.POST.get("tiket_entitled",False)
        destination = request.POST.get("destination",False)
        onward_journey = request.POST.get("onward_journey",False)
        return_journey = request.POST.get("return_journey",False)
        family_entry = request.POST.get("family_entry",False)
        attachment_file_status = 0
       
   
        

        



        











    pass



def user_apply_petty_cash(request):
    return render(request,'super_admin/user_apply_petty_cash.html')



def user_apply_advance_salary_request_from(request):

    return render(request,'super_admin/user_apply_advance_salary_request_from.html')



def user_view_leave_request(request):
    return render(request,'super_admin/user_view_leave_request.html')



def user_view_petty_cash(request):
    return render(request,'super_admin/user_view_petty_cash.html')



def user_view_advance_salary(request):
    return render(request,'super_admin/user_view_advance_salary.html')



@login_required(login_url='/index')
def role_management(request):
    
    
    status = inside_user_permission("Role",request.user)
    
    data = ""
    if(status['view_all'] == True):

    
        data = Role_details.objects.all().order_by('-id')
    elif (status['read'] == True):
        data = Role_details.objects.filter(auth_user=request.user).order_by('-id')

    
    return render(request,'super_admin/role_management.html',{'data':data,
        'write':status['write'],
        'edit':status['edit'],
        'delete':status['delete'],
        'read':status['read']
    })





def add_role_action(request):
    if request.method == "POST":
        role_name = request.POST.get("role_name",False)
        description = request.POST.get("description",False)
        role_status = request.POST.get("role_status",False)

        company_read = request.POST.get("company_read",False)
        company_write = request.POST.get("company_write",False)
        company_edit = request.POST.get("company_edit",False)
        company_delete = request.POST.get("company_delete",False)
        company_view_all = request.POST.get("company_view_all",False)
        company_manage_all = request.POST.get("company_manage_all",False)

        role_read = request.POST.get("role_read",False)
        role_write = request.POST.get("role_write",False)
        role_edit = request.POST.get("role_edit",False)
        role_delete = request.POST.get("role_delete",False)
        role_view_all = request.POST.get("role_view_all",False)
        role_manage_all = request.POST.get("role_manage_all",False)

        employee_read = request.POST.get("employee_read",False)
        employee_write = request.POST.get("employee_write",False)
        employee_edit = request.POST.get("employee_edit",False)
        employee_delete = request.POST.get("employee_delete",False)
        employee_view_all = request.POST.get("employee_view_all",False)
        employee_manage_all = request.POST.get("employee_manage_all",False)


        user_read = request.POST.get("user_read",False)
        user_write = request.POST.get("user_write",False)
        user_edit = request.POST.get("user_edit",False)
        user_delete = request.POST.get("user_delete",False)
        user_view_all = request.POST.get("user_view_all",False)
        user_manage_all = request.POST.get("user_manage_all",False)



        leave_read = request.POST.get("leave_read",False)
        leave_write = request.POST.get("leave_write",False)
        leave_edit = request.POST.get("leave_edit",False)
        leave_delete = request.POST.get("leave_delete",False)
        leave_view_all = request.POST.get("leave_view_all",False)
        leave_manage_all = request.POST.get("leave_manage_all",False)




        petty_read = request.POST.get("petty_read",False)
        petty_write = request.POST.get("petty_write",False)
        petty_edit = request.POST.get("petty_edit",False)
        petty_delete = request.POST.get("petty_delete",False)
        petty_view_all = request.POST.get("petty_view_all",False)
        petty_manage_all = request.POST.get("petty_manage_all",False)


        

        try:
            data_alredy_exist = Role_details.objects.get(role_name = role_name)
            context = {
                'message':'alredy_exists'
            }
            return render(request,'super_admin/role_management.html',context)

        except:
            pass
        data_save_role = Role_details.objects.create(
            auth_user = request.user,
            role_name = role_name,
            description = description,
            status = role_status
        )
        data_save_company_permission = Role_permission_details(
            role_id_id = data_save_role.id,
            permission_name = "Company",
            read = company_read,
            write = company_write,
            edit = company_edit,
            delete = company_delete,
            view_all = company_view_all,
            manage_all = company_manage_all,
            status = "True"
        )
        data_save_company_permission.save()




        data_save_petty_permission = Role_permission_details(
            role_id_id = data_save_role.id,
            permission_name = "Petty Cash",
            read = petty_read,
            write = petty_write,
            edit = petty_edit,
            delete = petty_delete,
            view_all = petty_view_all,
            manage_all = petty_manage_all,
            status = "True"
        )
        data_save_petty_permission.save()

        data_save_role_permission = Role_permission_details(
            role_id_id = data_save_role.id,
            permission_name = "Role",
            read = role_read,
            write = role_write,
            edit = role_edit,
            delete = role_delete,
            view_all = role_view_all,
            manage_all = role_manage_all,
            status = "True"
        )
        data_save_role_permission.save()

        data_save_employee_permission = Role_permission_details(
            role_id_id = data_save_role.id,
            permission_name = "Employee",
            read = employee_read,
            write = employee_write,
            edit = employee_edit,
            delete = employee_delete,
            view_all = employee_view_all,
            manage_all = employee_manage_all,
            status = "True"
        )
        data_save_employee_permission.save()

        data_save_user_permission = Role_permission_details(
            role_id_id = data_save_role.id,
            permission_name = "User",
            read = user_read,
            write = user_write,
            edit = user_edit,
            delete = user_delete,
            view_all = user_view_all,
            manage_all = user_manage_all,
            status = "True"
        )
        data_save_user_permission.save()





        data_save_leave_permission = Role_permission_details(
            role_id_id = data_save_role.id,
            permission_name = "Leave Management",
            read = leave_read,
            write = leave_write,
            edit = leave_edit,
            delete = leave_delete,
            view_all = leave_view_all,
            manage_all = leave_manage_all,
            status = "True"
        )
        data_save_leave_permission.save()

        # data = Role_details.objects.all()

        # context = {
        #     'message':'add_role',
        #     'data':data
        # }

        messages.success(request,str("success"))

        return redirect("role_management")







        
        


def view_role_more_details(request):
    id = request.GET.get("id",False)
    data = Role_details.objects.get(id=id)

    data_company_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Company")
    data_Role_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Role")
    data_Employee_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Employee")
    data_User_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="User")
    context = {
        'data':data,
        'data_company_permission':data_company_permission,
        'data_Role_permission':data_Role_permission,
        'data_Employee_permission':data_Employee_permission,
        'data_User_permission':data_User_permission
    }
    return render(request,'super_admin/view_role_more_details.html',context)


def edit_role_details(request):
    id = request.GET.get("id",False)
    data = Role_details.objects.get(id=id)

    data_company_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Company")
    data_Role_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Role")
    data_Employee_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Employee")
    data_User_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="User")
    data_leave_permission = ""
    try:
        data_leave_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Leave Management")
    except:
        pass

    data_petty_cash_permission = ""
    try:
        data_petty_cash_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Petty Cash")
    except:
        pass

    context = {
        'data':data,
        'data_company_permission':data_company_permission,
        'data_Role_permission':data_Role_permission,
        'data_Employee_permission':data_Employee_permission,
        'data_User_permission':data_User_permission,
        'data_leave_permission':data_leave_permission,
        'data_petty_cash_permission':data_petty_cash_permission
    }
    return render(request,'super_admin/edit_role_details.html',context)




def edit_role_details_action(request):
    if request.method == "POST":
        id = request.POST.get("id",False)
        role_name = request.POST.get("role_name",False)
        description = request.POST.get("description",False)
        role_status = request.POST.get("role_status",False)

        company_read = request.POST.get("company_read",False)
        company_write = request.POST.get("company_write",False)
        company_edit = request.POST.get("company_edit",False)
        company_delete = request.POST.get("company_delete",False)
        company_view_all = request.POST.get("company_view_all",False)
        company_manage_all = request.POST.get("company_manage_all",False)

        role_read = request.POST.get("role_read",False)
        role_write = request.POST.get("role_write",False)
        role_edit = request.POST.get("role_edit",False)
        role_delete = request.POST.get("role_delete",False)
        role_view_all = request.POST.get("role_view_all",False)
        role_manage_all = request.POST.get("role_manage_all",False)

        employee_read = request.POST.get("employee_read",False)
        employee_write = request.POST.get("employee_write",False)
        employee_edit = request.POST.get("employee_edit",False)
        employee_delete = request.POST.get("employee_delete",False)
        employee_view_all = request.POST.get("employee_view_all",False)
        employee_manage_all = request.POST.get("employee_manage_all",False)


        user_read = request.POST.get("user_read",False)
        user_write = request.POST.get("user_write",False)
        user_edit = request.POST.get("user_edit",False)
        user_delete = request.POST.get("user_delete",False)
        user_view_all = request.POST.get("user_view_all",False)
        user_manage_all = request.POST.get("user_manage_all",False)




        leave_read = request.POST.get("leave_read",False)
        leave_write = request.POST.get("leave_write",False)
        leave_edit = request.POST.get("leave_edit",False)
        leave_delete = request.POST.get("leave_delete",False)
        leave_view_all = request.POST.get("leave_view_all",False)
        leave_manage_all = request.POST.get("leave_manage_all",False)

        data_update_role = Role_details.objects.filter(id=id).update(role_name = role_name,
            description = description,
            status = role_status)

        data_update_company_permission = Role_permission_details.objects.filter(role_id_id=id, permission_name = "Company").update(
           
            read = company_read,
            write = company_write,
            edit = company_edit,
            delete = company_delete,
            view_all = company_view_all,
            manage_all = company_manage_all,
            status = "True"
        )

        try:
            alredy_exists = Role_permission_details.objects.get(role_id_id=id, permission_name = "Leave Management")

            data_update_leave_permission = Role_permission_details.objects.filter(role_id_id=id, permission_name = "Leave Management").update(
           
                read = leave_read,
                write = leave_write,
                edit = leave_edit,
                delete = leave_delete,
                view_all = leave_view_all,
                manage_all = leave_manage_all,
                status = "True"
            )
        except Role_permission_details.DoesNotExist:
            leave_save = Role_permission_details(
                role_id_id=id, permission_name = "Leave Management",
                read = leave_read,
                write = leave_write,
                edit = leave_edit,
                delete = leave_delete,
                view_all = leave_view_all,
                manage_all = leave_manage_all,
                status = "True"
            )
            leave_save.save()
            pass
        

        petty_read = request.POST.get("petty_read",False)
        petty_write = request.POST.get("petty_write",False)
        petty_edit = request.POST.get("petty_edit",False)
        petty_delete = request.POST.get("petty_delete",False)
        petty_view_all = request.POST.get("petty_view_all",False)
        petty_manage_all = request.POST.get("petty_manage_all",False)


        try:
            alredy_exists = Role_permission_details.objects.get(role_id_id=id, permission_name = "Petty Cash")

            data_update_leave_permission = Role_permission_details.objects.filter(role_id_id=id, permission_name = "Petty Cash").update(
           
                read = petty_read,
                write = petty_write,
                edit = petty_edit,
                delete = petty_delete,
                view_all = petty_view_all,
                manage_all = petty_manage_all,
                status = "True"
            )
        except Role_permission_details.DoesNotExist:
            leave_save = Role_permission_details(
                role_id_id=id, permission_name = "Petty Cash",
                read = petty_read,
                write = petty_write,
                edit = petty_edit,
                delete = petty_delete,
                view_all = petty_view_all,
                manage_all = petty_manage_all,
                status = "True"
            )
            leave_save.save()
            pass


        data_update_Role_permission = Role_permission_details.objects.filter(role_id_id=id, permission_name = "Role").update(
           
            read = role_read,
            write = role_write,
            edit = role_edit,
            delete = role_delete,
            view_all = role_view_all,
            manage_all = role_manage_all,
            status = "True"
        )

        data_update_Employee_permission = Role_permission_details.objects.filter(role_id_id=id, permission_name = "Employee").update(
           
            read = employee_read,
            write = employee_write,
            edit = employee_edit,
            delete = employee_delete,
            view_all = employee_view_all,
            manage_all = employee_manage_all,
            status = "True"
        )
        data_update_User_permission = Role_permission_details.objects.filter(role_id_id=id, permission_name = "User").update(
           
            read = user_read,
            write = user_write,
            edit = user_edit,
            delete = user_delete,
            view_all = user_view_all,
            manage_all = user_manage_all,
            status = "True"
        )

        return redirect(request.META['HTTP_REFERER'])


            



@test_w1('Company')
@login_required(login_url='/index')
def view_company_details(request):
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    company_data_url =api_domain+"api/get_companies"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            
        }
    })
    headers = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    response1 = requests.request("GET", company_data_url, headers=headers, data=payload).json()
    response12 = response1['result']
    response = response12['result']
    context = {
        'company_data' :response
    }
    return render(request,'super_admin/view_company_details.html',context)




async def odoo_employee_details_api(request,token,user_type):
    token_url = api_domain+"api/get_employees"
    print("user_type:::::",str(user_type))
    payload = json.dumps({ "jsonrpc": "2.0","params": {"login": "admin","password": "admin@veuz@123","db": "tss_migration_may14","is_admin":user_type}})
    headers =  {
        'api_key': token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url, headers=headers, data=payload) as res:
            response1 = await res.json()
            response12 =response1['result']
            return response12




@login_required(login_url='/index')
@test_w1('Employee')
def employee_master(request):
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    user_type = ''
    user_type_instance = User.objects.get(id=request.user.id)
    if user_type_instance.is_superuser  == True:
        user_type = True
    else:
        user_type = True
        print("----not admin user")

    response1 = asyncio.run(odoo_employee_details_api(request,odoo_token,user_type))
    print("response::::",str(response1))
    context = {
        'data':response1['result']
    }
    return  render(request,'super_admin/employee_master.html',context)



def employee_more_details(request):
    employee_id = request.GET.get("employee_id",False)
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    employee_data_url =api_domain+"api/get_employee"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id": employee_id
        }
    })
    headers = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    response = requests.request("GET", employee_data_url, headers=headers, data=payload)
    response_result = response.json()['result']
    data_response = response_result['result'][0]
    try:
        address_response = api_domain+"api/get_employee_address"
        address_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "address_home_id" : data_response['address_home_id'][0]
            }
        })
        address_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
    except:
        pass

    address_res = ""

    address_response1 = ""

    try:

        address_response = requests.request("GET", address_response, headers=address_headers, data=address_payload)
        address_res = address_response.json()['result']['result']

        address_response1 = address_res[0]

    except:

        pass

    

    context = {

        'response':data_response,

        'dept':"test",

        'address_response':address_response1,

        'state':"test",

        'country_id':"test"

    }

    return render(request,'super_admin/employee_more_details.html',context)










    


    

















from datetime import date


@login_required(login_url='/index')
@test_w1('User')
def user_management(request):
    message = request.GET.get("message",False)
    role_data = Role_details.objects.all()
    today = date.today()
    status = inside_user_permission("User",request.user)
    all_user_data = ""
    if(status['view_all'] == True):
        all_user_data = User_Management.objects.all().order_by("-id")
    elif (status['read'] == True):
        all_user_data = User_Management.objects.filter(add_by=request.user).order_by("-id")
    data_base_exists_employee_id = User_company_details.objects.all()
    data_exists_employee = list(data_base_exists_employee_id.values_list("odoo_id",flat=True))
    # params_data  = ",".join(data_exists_employee)
    select_employee_api = ""
    user_type = ''
    user_type_instance = User.objects.get(id=request.user.id)
    if user_type_instance.is_superuser  == True:
        user_type = True
    else:
        user_type = True
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    employee_data_url =api_domain+"api/get_employees"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
        "employee_ids": data_exists_employee,
        'is_admin':user_type,
        
        }
    })
    headers = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    select_employee_api1 = requests.request("GET", employee_data_url, headers=headers, data=payload)
    response_result = select_employee_api1.json()['result']
    select_employee_api = response_result['result']
    context = {
        'role_data':role_data,
        'message':message,
        'all_user_data':all_user_data,
        'select_employee_api':select_employee_api,
        'today':today,
        'write':status['write'],
        'edit':status['edit'],
        'delete':status['delete'],
        'read':status['read']
        
    }
    return render(request,'super_admin/user_management.html',context)


def getemployee_branch_dpt(request):
    employee_id = request.GET.get("employee_id")
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    employee_data_url =api_domain+"api/get_employee"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id": int(employee_id)
        }
    })
    headers = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    response1  = requests.request("GET", employee_data_url, headers=headers, data=payload).json()
    response12 =response1['result']
    print(response12)
    response = response12['result'][0]
    name = ""
    employee_dpt = ""
    employee_branch = ""
    emp_registration_id = ""
    name = response['name']
    company_name = response['company_id']
    username = response['user_name']
    image_1920 = response['image_1920']
    company_id = ''
    branch_id = ''
    multiple_company_details = response['branch_list']
    try:
        employee_dpt  = response['department_id'][1]
        if employee_dpt == "false":
            employee_dpt = ""
    except:
        employee_dpt = False
    try:
        employee_branch = response['branch_id'][1]
        branch_id = response['branch_id'][0]
        if  employee_branch == "false":
            employee_branch = ""

    except:
        employee_branch = False
        
    emp_registration_id = response['registration_number']
    user_edit_status = False
    if User.objects.filter(username=username).exists():
        user_edit_status = True
    data = {
        "employee_branch" :employee_branch,
        "employee_dpt":employee_dpt,
        "employee_name":name,
        "emp_registration_id":emp_registration_id,
        'company_name':str(company_name[1]),
        'username':username,
        'image_1920':image_1920,
        'user_edit_status':user_edit_status,
        'odoo_employee_company_id' :company_name[0],
        'odoo_employee_branch_id' :branch_id,
        'multiple_company_details':multiple_company_details
    }
    return JsonResponse(data,safe=False)




def user_management1(message):
    message = request.GET.get("message",False)
    role_data = Role_details.objects.all()

    all_user_data = User_Management.objects.all()
    context = {
        'role_data':role_data,
        'message':message,
        'all_user_data':all_user_data
    }
    return render(request,'super_admin/user_management.html',context)



def user_add_action(request):
    if request.method == "POST":
        import time
        odoo_employee_company_id = request.POST.get("odoo_employee_company_id",False)
        odoo_employee_branch_id = request.POST.get("odoo_employee_branch_id",False)
        username = request.POST.get("username",False)
        password_option = request.POST.get("password_option",False)
        image_1920 = request.POST.get("image_1920",False)
        if User.objects.filter(username=username).exists():
            messages.warning(request,str("An account with the given username alredy exists"))
            return redirect("user_management")

        if password_option == "Automatic":
            import string    
            import random
            S = 10
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        else:
            password = request.POST.get("password",False)
        
        
        description = request.POST.get("description",False)
        password_expiration_status = request.POST.get("password_expiration_status",False)
        effective_from_dt = request.POST.get("password_effective_from_dt",False)
        effective_to_dt = request.POST.get("password_effective_to_dt",False)
        
        if effective_to_dt == "":
            effective_to_dt = None
        employee_branch = request.POST.get("employee_branch",False)
        
         
        employee_id = request.POST.get("employee_id",False)
       

        if employee_id == '0':
            
            pass
        else:
            
            if employee_branch == "false":
                messages.warning(request,str("An Branch is required or has an invalid value, please correct and try again!!!"))
                return redirect("user_management")
            elif employee_branch == "":
                messages.warning(request,str("An Branch is required or has an invalid value, please correct and try again!!!"))
                return redirect("user_management")

                
            

        

        
        
        employee_department = request.POST.get("employee_department",False)
        employee_name = request.POST.get("employee_name",False)

        role_id = request.POST.getlist("role_id[]")
        role_description = request.POST.getlist("role_description[]")
        role_start_dt = request.POST.getlist("role_start_dt[]")
        role_end_dt = request.POST.getlist("role_end_dt[]")
        company_name = request.POST.get("company_name",False)
        

        role_length = len(role_id)
        

        emp_registration_id = request.POST.get("emp_registration_id",False)

       

        if password_expiration_status == "days":
            passsword_used_days = request.POST.get("passsword_used_days",False)
            

            from datetime import timedelta, date
            EndDate = date.today() + timedelta(days=int(passsword_used_days))
            
            try:
                user_alredy_exists_condition = User_Management.objects.get(employee_id=employee_id)
                if user_alredy_exists_condition is not None:
                   pass
                
                url = redirect("user_management")
                
        
                return HttpResponseRedirect(url.url + '?message=' + "already_exists")
            except User_Management.DoesNotExist:

                if employee_id == 0:
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    data1 = Token.objects.create(user=user)
                    
                    save_user_data = User_Management.objects.create(
                        auth_user = user,
                        username = username,
                        password_option = password_option,
                        password = password,
                        description = description,
                        password_expiration_status = password_expiration_status,
                        password_expiration_total_days = passsword_used_days,
                        password_expiration_end_date = EndDate,
                        effective_from_dt = effective_from_dt,
                        effective_to_dt = effective_to_dt,
                        employee_id = "False",
                        employee_branch = employee_branch,
                        employee_department = employee_department,
                        employee_name = employee_name,
                        status = "True",
                        add_by = request.user,
                        odoo_id = "False",
                        company_name = company_name,
                        user_img = image_1920,
                        



                    )
                    for i in range(0,role_length):

                        role_end_dt1 = role_end_dt[i]
                        if role_end_dt1 == "":
                            role_end_dt1 = None
                        data_save_user_role = user_role_mapping(
                            auth_user_id = user,
                            user_id_id = save_user_data.id,
                            role_id_id = role_id[i],
                            start_dt = role_start_dt[i],
                            end_dt = role_end_dt1,
                            description = role_description[i]
                        )
                        data_save_user_role.save()
                   
                       

                


                else:
                   
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    data1 = Token.objects.create(user=user)
                    
                    save_user_data = User_Management.objects.create(
                        auth_user = user,
                        username = username,
                        password_option = password_option,
                        password = password,
                        description = description,
                        password_expiration_status = password_expiration_status,
                        password_expiration_total_days = passsword_used_days,
                        password_expiration_end_date = EndDate,
                        effective_from_dt = effective_from_dt,
                        effective_to_dt = effective_to_dt,
                        employee_id = emp_registration_id,
                        employee_branch = employee_branch,
                        employee_department = employee_department,
                        employee_name = employee_name,
                        status = "True",
                        add_by = request.user,
                        odoo_id = employee_id,
                        company_name = company_name,
                        user_img = image_1920,
                        employee_branch_id = odoo_employee_branch_id,
                        employee_company_id = odoo_employee_company_id


                    )
                    for i in range(0,role_length):
                        role_end_dt1 = role_end_dt[i]
                        if role_end_dt1 == "":
                            role_end_dt1 = None
                        data_save_user_role = user_role_mapping(
                            auth_user_id = user,
                            user_id_id = save_user_data.id,
                            role_id_id = role_id[i],
                            start_dt = role_start_dt[i],
                            end_dt = role_end_dt1,
                            description = role_description[i]
                        )
                        data_save_user_role.save()

                    multi_company_id = request.POST.getlist("multi_company_id[]")
                    multi_company_name = request.POST.getlist("multi_company_name[]")
                    multiple_branch = request.POST.getlist("multiple_branch[]")
                    multiple_branch_id = request.POST.getlist("multiple_branch_id[]")
                    multi_company_employee_id = request.POST.getlist("multi_company_employee_id[]")
                    role_length = len(multi_company_id)
                    for i in range(0,role_length):
                        multiple_branch_name =str(multiple_branch[i][0:-1])
                        branch_List = multiple_branch_name.split(',')
                        branch_List_length = len(branch_List)
                        if i == 0:
                            save_multiple_company_instance = User_company_details.objects.create(auth_user_id=user,user_id_id=save_user_data.id,company_name=str(multi_company_name[i]),company_id=int(multi_company_id[i]),status=True,odoo_id=int(multi_company_employee_id[i]))
                            for j in range(0,branch_List_length):
                                if j == 0:
                                    l1 = str(branch_List[j])
                                    branch_list = str(l1).split('&')
                                    save_multiple_company_based_branch_instance = User_company_based_branch_details(company_id_id=save_multiple_company_instance.id,branch_name=str(branch_list[0]),branch_id=int(branch_list[1]),status=True)
                                    save_multiple_company_based_branch_instance.save()
                                else:
                                    l1 = str(branch_List[j])
                                    branch_list = str(l1).split('&')
                                    save_multiple_company_based_branch_instance = User_company_based_branch_details(company_id_id=save_multiple_company_instance.id,branch_name=str(branch_list[0]),branch_id=int(branch_list[1]),status=False)
                                    save_multiple_company_based_branch_instance.save()
                        else:
                            save_multiple_company_instance = User_company_details.objects.create(auth_user_id=user,user_id_id=save_user_data.id,company_name=str(multi_company_name[i]),company_id=int(multi_company_id[i]),status=False,odoo_id=int(multi_company_employee_id[i]))
                            for j in range(0,branch_List_length):
                                l1 = str(branch_List[j])
                                branch_list = str(l1).split('&')
                                save_multiple_company_based_branch_instance = User_company_based_branch_details(company_id_id=save_multiple_company_instance.id,branch_name=str(branch_list[0]),branch_id=int(branch_list[1]),status=False)
                                save_multiple_company_based_branch_instance.save()


                        

                       
                
                # url = redirect("user_management")
                # print("url", url.url)
                messages.success(request,str("success"))
                return redirect("user_management")
                # return HttpResponseRedirect(url.url + '?message=' + "added")

            pass

        elif password_expiration_status == "none":
            try:
                user_alredy_exists_condition = User_Management.objects.get(employee_id=employee_id)
                if user_alredy_exists_condition is not None:
                    pass
                   
                
                url = redirect("user_management")
                
        
                return HttpResponseRedirect(url.url + '?message=' + "already_exists")

            except User_Management.DoesNotExist:
                
                if employee_id == 0:
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    data1 = Token.objects.create(user=user)
                    
                    save_user_data = User_Management.objects.create(
                        auth_user = user,
                        username = username,
                        password_option = password_option,
                        password = password,
                        description = description,
                        password_expiration_status = password_expiration_status,
                        effective_from_dt = effective_from_dt,
                        effective_to_dt = effective_to_dt,
                        employee_id = "False",
                        employee_branch = employee_branch,
                        employee_department = employee_department,
                        employee_name = employee_name,
                        status = "True",
                        add_by = request.user,
                        odoo_id = "False",
                        company_name = company_name,
                        user_img = image_1920


                    )
                    for i in range(0,role_length):
                        data_save_user_role = user_role_mapping(
                            auth_user_id = user,
                            user_id_id = save_user_data.id,
                            role_id_id = role_id[i],
                            start_dt = role_start_dt[i],
                            end_dt = role_end_dt[i],
                            description = role_description[i]
                        )
                        data_save_user_role.save()
                   
                       
                else:
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    data1 = Token.objects.create(user=user)
                    
                    save_user_data = User_Management.objects.create(
                        auth_user = user,
                        username = username,
                        password_option = password_option,
                        password = password,
                        description = description,
                        password_expiration_status = password_expiration_status,
                        effective_from_dt = effective_from_dt,
                        effective_to_dt = effective_to_dt,
                        employee_id = emp_registration_id,
                        employee_branch = employee_branch,
                        employee_department = employee_department,
                        employee_name = employee_name,
                        status = "True",
                        add_by = request.user,
                        odoo_id = employee_id,
                        company_name = company_name,
                        user_img = image_1920,
                        employee_branch_id = odoo_employee_branch_id,
                        employee_company_id = odoo_employee_company_id


                    )
                    for i in range(0,role_length):
                        role_end_dt1 = role_end_dt[i]
                        if role_end_dt1 == "":
                            role_end_dt1 = None
                        data_save_user_role = user_role_mapping(
                            auth_user_id = user,
                            user_id_id = save_user_data.id,
                            role_id_id = role_id[i],
                            start_dt = role_start_dt[i],
                            end_dt = role_end_dt1,
                            description = role_description[i]
                        )
                        data_save_user_role.save()

                    multi_company_id = request.POST.getlist("multi_company_id[]")
                    multi_company_name = request.POST.getlist("multi_company_name[]")
                    multiple_branch = request.POST.getlist("multiple_branch[]")
                    multiple_branch_id = request.POST.getlist("multiple_branch_id[]")
                    multi_company_employee_id = request.POST.getlist("multi_company_employee_id[]")
                    role_length = len(multi_company_id)
                    for i in range(0,role_length):
                        multiple_branch_name =str(multiple_branch[i][0:-1])
                        branch_List = multiple_branch_name.split(',')
                        branch_List_length = len(branch_List)
                        if i == 0:
                            save_multiple_company_instance = User_company_details.objects.create(auth_user_id=user,user_id_id=save_user_data.id,company_name=str(multi_company_name[i]),company_id=int(multi_company_id[i]),status=True,odoo_id=int(multi_company_employee_id[i]))
                            for j in range(0,branch_List_length):
                                if j == 0:
                                    l1 = str(branch_List[j])
                                    branch_list = str(l1).split('&')
                                    save_multiple_company_based_branch_instance = User_company_based_branch_details(company_id_id=save_multiple_company_instance.id,branch_name=str(branch_list[0]),branch_id=int(branch_list[1]),status=True)
                                    save_multiple_company_based_branch_instance.save()
                                else:
                                    l1 = str(branch_List[j])
                                    branch_list = str(l1).split('&')
                                    save_multiple_company_based_branch_instance = User_company_based_branch_details(company_id_id=save_multiple_company_instance.id,branch_name=str(branch_list[0]),branch_id=int(branch_list[1]),status=False)
                                    save_multiple_company_based_branch_instance.save()
                        else:
                            save_multiple_company_instance = User_company_details.objects.create(auth_user_id=user,user_id_id=save_user_data.id,company_name=str(multi_company_name[i]),company_id=int(multi_company_id[i]),status=False,odoo_id=int(multi_company_employee_id[i]))
                            for j in range(0,branch_List_length):
                                l1 = str(branch_List[j])
                                branch_list = str(l1).split('&')
                                save_multiple_company_based_branch_instance = User_company_based_branch_details(company_id_id=save_multiple_company_instance.id,branch_name=str(branch_list[0]),branch_id=int(branch_list[1]),status=False)
                                save_multiple_company_based_branch_instance.save()

                        
                messages.success(request,str("password:"+str(password)))
                return redirect("user_management")







     

        



def view_user_more_details(request):

    id = request.GET.get("id",False)
   
    data = User_Management.objects.get(id=id)

    user_role_details = user_role_mapping.objects.filter(user_id_id=id)
    data_company = User_company_details.objects.filter(user_id_id=id)

    context = {
        'data':data,
        'user_role_details':user_role_details,
        'data_company':data_company
    }
    return render(request,'super_admin/view_user_more_details.html',context)




def edit_user_more_details(request):
    id = request.GET.get("id",False)
    

    data = User_Management.objects.get(id=id)

    user_role_details = user_role_mapping.objects.filter(user_id_id=id)


    role_data = Role_details.objects.all()




    context = {
        'data':data,
        'user_role_details':user_role_details,
        'role_data':role_data
    }
    return render(request,'super_admin/edit_user_more_details.html',context)





def test_update_auth_user_table(request):
    u = User.objects.get(username='admin1')
    u.set_password('admin1')
    u.save()

    # update = User.objects.filter(id=request.user.id).update(username="admin",password="123")



def check_user_role_updated_or_not(role_id,value,updated_field_name):
    
    if updated_field_name == "description":

        try:
            data_alredy_exists = user_role_mapping.objects.get(id=role_id,description=value)
            return False
        except user_role_mapping.DoesNotExist:
            return True
    elif updated_field_name == "start_dt":
        try:
            data_alredy_exists = user_role_mapping.objects.get(id=role_id,start_dt=value)
            return False
        except user_role_mapping.DoesNotExist:
            return True
    elif updated_field_name == "end_dt":
        try:
            data_alredy_exists = user_role_mapping.objects.get(id=role_id,end_dt=value)
            return False
        except user_role_mapping.DoesNotExist:
            return True





def edit_user_details_action(request):
    if request.method == "POST":
        user_updated_id = request.POST.get("user_updated_id",False)
        user_status = request.POST.get("user_status",False)

        print("user_status::::",str(user_status))
        if user_status == "True":
             data_update = User_Management.objects.filter(id=user_updated_id).update(login_password_invalid_count=0,status=True)
        else:
            data_update = User_Management.objects.filter(id=user_updated_id).update(status=False)


        



        
        username = request.POST.get("username",False)
        password_option = request.POST.get("edit_password_option",False)
        if password_option == "Automatic":
            password = request.POST.get("password",False)
            pass
            # import string    
            # import random
            # S = 10
            # password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        else:
            password = request.POST.get("password",False)

        employee_branch = request.POST.get("employee_branch",False)
        employee_department = request.POST.get("employee_department",False)
        employee_name = request.POST.get("employee_name",False)
        description = request.POST.get("description",False)
        edit_password_expiration = request.POST.get("edit_password_expiration",False)


       
        edit_passsword_used_days = request.POST.get("edit_passsword_used_days",False)
        password_effective_from_dt = request.POST.get("password_effective_from_dt",False)

        password_effective_to_dt = request.POST.get("password_effective_to_dt",False)
        if password_effective_to_dt == "":
            password_effective_to_dt = None
        if edit_password_expiration == "days":

            try:
                check_days_alredy_exists = User_Management.objects.get(id=user_updated_id,password_expiration_status="days",password_expiration_total_days=edit_passsword_used_days)
                if check_days_alredy_exists is not None:
                    user_details = User_Management.objects.get(id=user_updated_id)

                    u = User.objects.get(id=user_details.auth_user.id)
                    u.set_password(password)
                    u.save()
                    update_auth_username = User.objects.filter(id=user_details.auth_user.id).update(username=username)
                    updte_days = User_Management.objects.filter(id=user_updated_id).update(
                    username = username,
                    password_option = password_option,
                    password = password,
                    description = description,
                    password_expiration_status = edit_password_expiration,
                    effective_from_dt = password_effective_from_dt,
                    effective_to_dt = password_effective_to_dt,
                    employee_branch =employee_branch,
                    employee_department = employee_department,
                    employee_name = employee_name

                
                    )
                    


                    pass
                    

            except User_Management.DoesNotExist:
                from datetime import timedelta, date
                EndDate = date.today() + timedelta(days=int(edit_passsword_used_days))
              
                user_details = User_Management.objects.get(id=user_updated_id)

                u = User.objects.get(id=user_details.auth_user.id)
                u.set_password(password)
                u.save()
                update_auth_username = User.objects.filter(id=user_details.auth_user.id).update(username=username)
                updte_days = User_Management.objects.filter(id=user_updated_id).update(
                    username = username,
                    password_option = password_option,
                    password = password,
                    description = description,
                    password_expiration_status = edit_password_expiration,
                    password_expiration_total_days = edit_passsword_used_days,
                    password_expiration_end_date = EndDate,
                    effective_from_dt = password_effective_from_dt,
                    effective_to_dt = password_effective_to_dt,
                    employee_branch =employee_branch,
                    employee_department = employee_department,
                    employee_name = employee_name

                
                )
                
                pass
            pass

        elif edit_password_expiration == "none":
            data_user_details = User_Management.objects.filter(id=user_updated_id).update(
                username = username,
                password_option = password_option,
                password = password,
                description = description,
                password_expiration_status = edit_password_expiration,
                effective_from_dt = password_effective_from_dt,
                effective_to_dt = password_effective_to_dt,
                employee_branch = employee_branch,
                employee_department = employee_department,
                employee_name = employee_name,
                password_expiration_total_days=None

                
            )

            user_details = User_Management.objects.get(id=user_updated_id)

            u = User.objects.get(id=user_details.auth_user.id)
            u.set_password(password)
            u.save()
            update_auth_username = User.objects.filter(id=user_details.auth_user.id).update(username=username)
            pass




        



        role_data = user_role_mapping.objects.filter(user_id_id=user_updated_id)
       
        for i in role_data:





            edit_role_description_data = request.POST.get("edit_role_description_data"+str(i.id))
            edit_role_start_date_data = request.POST.get("edit_role_start_date_data"+str(i.id))
            edit_role_end_date_data = request.POST.get("edit_role_end_date_data"+str(i.id))
            if edit_role_end_date_data == "":
                edit_role_end_date_data = None
            description_result = check_user_role_updated_or_not(i.id,edit_role_description_data,"description")
            start_date_result = check_user_role_updated_or_not(i.id,edit_role_start_date_data,"start_dt")
            end_date_result = check_user_role_updated_or_not(i.id,edit_role_end_date_data,"end_dt")
            
            

            update_data = user_role_mapping.objects.filter(id=i.id).update(
                description = edit_role_description_data,
                start_dt = edit_role_start_date_data,
                end_dt = edit_role_end_date_data

            )
            if description_result == True or start_date_result == True or end_date_result == True:
               

                log_start_dt = ""
                if start_date_result == True:
                    log_start_dt = edit_role_start_date_data
                else:
                    log_start_dt = None
                log_end_dt = ""
                if end_date_result == True:
                    log_end_dt = edit_role_end_date_data
                else:
                    log_end_dt = None
                
                log_description = ""
                if description_result == True:
                    log_description = edit_role_description_data
                else:
                    log_description = None
                
                data_save_log = user_role_mapping_history(
                    user_role_mapping_id_id = i.id,
                    start_dt = log_start_dt,
                    end_dt = log_end_dt,
                    updated_by = request.user,
                    description = log_description,
                    status = "True"
                )
                data_save_log.save()



            else:
                pass
            

        



        add_edit_role_id = request.POST.getlist('edit_role_id[]')
        add_edit_role_description = request.POST.getlist("edit_role_description[]")
        add_edit_role_start_dt = request.POST.getlist("edit_role_start_dt[]")
        add_edit_role_end_dt = request.POST.getlist("edit_role_end_dt[]")
       

        total_add_role_len = len(add_edit_role_id)
        user_data = User_Management.objects.get(id=user_updated_id)
        
        for add_role in range(0,total_add_role_len):
            add_edit_role_end_dt1 =add_edit_role_end_dt[add_role]
            if add_edit_role_end_dt1 == "":
                add_edit_role_end_dt1 = None
            add_role_data = user_role_mapping(
                auth_user_id = user_data.auth_user,
                user_id_id = user_updated_id,
                role_id_id = add_edit_role_id[add_role],
                start_dt = add_edit_role_start_dt[add_role],
                end_dt = add_edit_role_end_dt1,
                description = add_edit_role_description[add_role],
                status = "True"

            )
            add_role_data.save()
            pass
        
        
        return redirect(request.META['HTTP_REFERER'])

        pass





def test_api(request):
    

    response = requests.get("http://10.10.10.107:8069/api/get_all_employees").json()

    return render(request,'super_admin/test_api.html',{'response':response})





def update_user_role_permission_action(request):
    if request.method == "POST":
        update_role_id = request.POST.get("update_role_id",False)
        update_role_start_dt = request.POST.get("update_role_start_dt",False)
        update_role_end_dt = request.POST.get("update_role_end_dt",False)
        update_role_description = request.POST.get("update_role_description",False)
        data_update_role = user_role_mapping.objects.filter(id=update_role_id).update(
            start_dt = update_role_start_dt,
            end_dt = update_role_end_dt,
            description = update_role_description
        )
        return redirect(request.META['HTTP_REFERER'])


def user_role_delete_action(request):
    if request.method == "POST":
        role_id = request.POST.get("role_id",False)
        data_delete = user_role_mapping.objects.get(id=role_id)
        data_delete.delete()
        return redirect(request.META['HTTP_REFERER'])




def user_add_new_role_action(request):
    if request.method == "POST":
        add_role_user_id = request.POST.get("add_role_user_id",False)
        add_role_id = request.POST.get("add_role_id",False)
        add_role_start_dt = request.POST.get("add_role_start_dt",False)
        add_role_end_dt = request.POST.get("add_role_end_dt",False)
        add_role_description = request.POST.get("add_role_description",False)
        user_data = User_Management.objects.get(id=add_role_user_id)
        data_add_role = user_role_mapping(
            auth_user_id_id= user_data.auth_user.id,
            user_id_id  = add_role_user_id,
            role_id_id = add_role_id,
            start_dt = add_role_start_dt,
            end_dt = add_role_end_dt,
            description = add_role_description,
            status = "True"
        )
        data_add_role.save()
        return redirect(request.META['HTTP_REFERER'])









async def odoo_leave_history_api(request,odoo_id,token):
    token_url = api_domain+"api/get_leave_history"
    payload = json.dumps({ "jsonrpc": "2.0","params": {"employee_id": int(odoo_id)}})
    print("hhhhhhhhhhhhhhhhhhhh")
    headers ={'api_key': token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url, headers=headers, data=payload) as res:
            response1 = await res.json()
            response12 =response1['result']['result']
            print("hhhhhhhhhhhhhhhhhhqqqqqqqqqhh")
            return response12
    pass

async def odoo_leave_leave_type_api(request,token):
    token_url = api_domain+"api/get_leave_types"
    payload = json.dumps({ "jsonrpc": "2.0","params": {}})
    headers ={'api_key': token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url, headers=headers, data=payload) as res:
            response1 = await res.json()
            response12 =response1['result']['result']
            return response12
    pass

async def odoo_leave_replacer_api(request,token):
    token_url = api_domain+"api/get_employees"
    payload = json.dumps({ "jsonrpc": "2.0","params": {}})
    headers ={'api_key':token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url, headers=headers, data=payload) as res:
            response1 = await res.json()
            response12 =response1['result']['result']
            return response12
    pass

async def odoo_leave_child_response_api(request,odoo_id,token):
    token_url =  api_domain+"api/get_childs"
    payload = json.dumps({ "jsonrpc": "2.0","params": { "employee_id" : int(odoo_id)}})
    headers ={'api_key': token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url, headers=headers, data=payload) as res:
            response1 = await res.json()
            response12 =response1['result']['result']
            return response12
    pass

async def odoo_leave_entitlement_balances_response_api(request,odoo_id,token):
    token_url =  api_domain+"api/get_leave_entitlement"
    payload = json.dumps({ "jsonrpc": "2.0","params": { "employee_id" : int(odoo_id)}})
    headers ={'api_key': token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url, headers=headers, data=payload) as res:
            response1 = await res.json()
            response12 =response1['result']['result']
            return response12
    pass





async def odoo_new_leave_api(request,odoo_id,token):
    token_url =  api_domain+"api/get_leave"
    payload = json.dumps({ "jsonrpc": "2.0","params": { "employee_id" : int(odoo_id)}})
    headers ={'api_key': token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url, headers=headers, data=payload) as res:
            response1 = await res.json()
            # print("response1::::",str(response1))
            response12 =response1['result']['result']
            return response12
    pass

@login_required(login_url='/index')
def leave_management(request):
    user_auth_id = request.user.id
    odoo_id = 0
    emp_name = ""
    emp_email = ""
    emp_id = ""
    try:
        odoo_data = User_Management.objects.get(auth_user=user_auth_id)
        odoo_id = odoo_data.odoo_id
        emp_name = odoo_data.employee_name
        emp_email = odoo_data.username
        emp_id = odoo_data.employee_id
    except:
        pass
    print("odoo_id112222::::",str(odoo_id))
    leave_history_response = ""
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    new_api_integration =  asyncio.run(odoo_new_leave_api(request,odoo_id,odoo_token_data.token))
    leave_history_response = new_api_integration['leave_history']
    leave_type_response = new_api_integration['leave_types']
    entitlement_balances_response = new_api_integration['entitled_details']
    replacer_response = new_api_integration['possible_replacers']
    child_response = new_api_integration['childs_ids_with_current_empl']

    draf_leave_details = User_leave_draf_history.objects.filter(auth_user_id=request.user,status="pending")
    context = {
        'leave_type_response':leave_type_response,
        'leave_history_response':leave_history_response,
        'emp_name':emp_name,
        'emp_email':emp_email,
        'emp_id':emp_id,
        'replacer_response':replacer_response,
        'child_response':child_response,
        'entitlement_balances_response':entitlement_balances_response,
        'child_count':len("child_response"),
        'draf_leave_details':draf_leave_details,
        'odoo_id':odoo_id
        
    }

    return render(request,'super_admin/leave_management.html',context)
   
    
   



    
   


   
    


   



def get_total_available_leave_count(request):

    leave_type = request.GET.get("leave_type",False)
    selected_employee_id = request.GET.get("selected_employee_id",False)
    odoo_login_id = 0
    print("leave_type::::",str(leave_type))
    print("selected_employee_id:::",str(selected_employee_id))
    half_day_status = ""
    try:
        user_data = User_Management.objects.get(auth_user=request.user.id)
        odoo_login_id = user_data.odoo_id
    except:
        pass
    leave_available_response = ""
    respose_status= ""
    requires_allocation = ""
    try:
        odoo_token_data = odoo_api_request_token.objects.get(status="True")
        odoo_token = odoo_token_data.token
        leave_available_url =api_domain+"api/get_remaining_leaves_by_type"
        payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id" : int(selected_employee_id),
                "type_id" : int(leave_type)
            }
        })
        headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        leave_available_response1 = requests.request("GET", leave_available_url, headers=headers, data=payload).json()
        leave_available_response12 = leave_available_response1['result']
        response_message = leave_available_response12['message']
       
        respose_status = response_message
        leave_available_response = leave_available_response12['result']
        half_day_status = leave_available_response['request_unit']
        requires_allocation = leave_available_response['requires_allocation']
        support_document = leave_available_response['support_document']
        print("support_document::;;;",support_document)
    except:
        pass
    leave_type_name = ""
    total_available_leave = 0
    annual_status = False
    try:
       
        leave_type_name = str(leave_available_response['type_name'])
        total_available_leave = str(leave_available_response['remaining_leaves'])
        annual_status = leave_available_response[0]['is_annual_vacation']
       
    except:
        pass
    
    data= {
        'respose_status':respose_status,
        'total_available_leave' :total_available_leave ,
        'leave_type_name':leave_type_name,
        'annual_status':annual_status,
        'half_day_status':half_day_status,
        'requires_allocation':requires_allocation,
        'support_document' : support_document
    }
       
    return JsonResponse(data,safe=False)



async def new_supplier_api(request,list_data,odoo_token):
    supplier =  api_domain+"api/get_employees"
    payload = json.dumps({"jsonrpc": "2.0","params": {"employee_ids": list_data}})
    headers ={'api_key': odoo_token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(supplier, headers=headers, data=payload) as res:
            response1 = await res.json()
            response_result = response1['result']
            return response_result
    pass

async def new_jobno_api(request,list_data,odoo_token):
    job_no =  api_domain+"api/get_employees"
    payload = json.dumps({ "jsonrpc": "2.0","params": { "employee_ids": list_data}})
    headers ={'api_key': odoo_token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(job_no, headers=headers, data=payload) as res:
            response1 = await res.json()
            response_result = response1['result']
            return response_result
    pass


async def petty_cash_details_api_request(request,employee_id,odoo_token):
    url = api_domain+""
    payload = json.dumps({ "jsonrpc": "2.0","params": { "employee_ids": employee_id}})
    headers ={'api_key': odoo_token,'Content-Type': 'application/json','Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, data=payload) as res:
            response1 = await res.json()
            response_result = response1['result']
            return response_result



@test_w1('Petty Cash')
def petty_cash_management(request):
    employee_id = ''
    try:
        odoo_data = User_Management.objects.get(auth_user=request.user)
        employee_id = odoo_data.odoo_id
    except:
        pass
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    new_api_integration = ''
    try:
        new_api_integration =  asyncio.run(petty_cash_details_api_request(request,employee_id,odoo_token_data.token))
    except:
        pass
    select_supplier_api = ''
    select_job_no = ''
    view_petty_cash_details =''
    existing_amount = ''
    try:
        select_supplier_api = new_api_integration['select_supplier_api']
        select_job_no= new_api_integration['select_job_no']
        view_petty_cash_details = new_api_integration['view_petty_cash_details']
        existing_amount = new_api_integration['existing_amount']
    except:
        pass
    
    





    context = {
        'select_supplier_api':select_supplier_api,
        'select_job_no':select_job_no
    }
    return render(request,'super_admin/petty_cash_management.html',context)



def advance_salary_management(request):
    return render(request,'super_admin/advance_salary_management.html')


def role_edit_modal_function(request):
    id = request.GET.get("id",False)
   
    data = Role_details.objects.get(id=id)

    data_company_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Company")
    data_Role_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Role")
    data_Employee_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Employee")
    data_User_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="User")
    data_leave_permission = ""
    try:
        data_leave_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Leave Management")
    except:
        pass

    data_petty_cash_permission = ""
    try:
        data_petty_cash_permission = Role_permission_details.objects.get(role_id_id=id,permission_name="Petty Cash")
    except:
        pass

    context = {
        'data':data,
        'data_company_permission':data_company_permission,
        'data_Role_permission':data_Role_permission,
        'data_Employee_permission':data_Employee_permission,
        'data_User_permission':data_User_permission,
        'data_leave_permission':data_leave_permission,
        'data_petty_cash_permission':data_petty_cash_permission
    }
    return render(request,'super_admin/role_edit_modal_function.html',context)




def user_edit_modal_function(request):
    id = request.GET.get("id",False)
   
    data = User_Management.objects.get(id=id)

    user_role_details = user_role_mapping.objects.filter(user_id_id=id)


    role_data = Role_details.objects.all()

    today = date.today()


    context = {
        'data':data,
        'user_role_details':user_role_details,
        'role_data':role_data,
        'today':today
    }

    return render(request,'super_admin/user_edit_modal_function.html',context)



def user_role_log_modal(request):
    id = request.GET.get("id",False)
  

    data_history = user_role_mapping_history.objects.filter(user_role_mapping_id_id=id).order_by("-id")
    context = {
        'data_history':data_history
    }
    return render(request,'super_admin/user_role_log_modal.html',context)





m1 = "null" 

from django.contrib import messages
def test_r1(request):
    return render(request,'super_admin/t1.html')
    # global m1
    # m1 = "suceess"
    
    
    

    

    
    # messages.success(request, 'Passwords are not same.!')
    # return redirect('testr1')

def testr1(request):
    if request.method == "POST":
        name = request.POST.get("name",False)
       
        messages.success(request, 'Passwords are not same.!')
        return redirect('index')
    
    return render(request,'super_admin/index.html')




def send_push_notification(send_user_id,leave_request_username):
    print("send_user_id::",str(send_user_id))

    user__id = send_user_id
    message = "one leave request from " +leave_request_username
    user1 = user_fcm_token.objects.get(user = user__id)
    token = user1.fcm_token
    print("token::::",str(token))
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
        "title":"Leave Approve Request",
                "body":message,
                "icon" : "https://erp.veuz.in/static/hrm/images/logo.png"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=AAAAlgMZ980:APA91bFD9Uvem1jR8y_DMeHtpGVHPfsE-mspG6SlivhobgxSHouKlcshoAm-kmwujx1mX-dDwuJY-H9zZsY3llo1CcgUq3DNDj9SHs2gbxpkPOPa07RDtyHYRvTaiwnhlAwPkb9PDzEg"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    print("notification send message:::")
    print(data.text)
    pass





from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_file_upload_ajax(request):
    print("heyyyyyyyyyyyyyyyyyyy")
    employee_attached_file = request.FILES['employee_attached_file']
    name = request.POST.get("name")
    print("name:::::",str(name))
    print("employee_attached_file:::::::::",str(employee_attached_file))

    data_save = test_file_upload(
        file_data = employee_attached_file
    )
    data_save.save()
    print("employee_attached_file:::::",str(employee_attached_file))


@csrf_exempt
def user_leave_apply_action(request):
    if request.method == "POST":
        image_byte_code = request.POST.get("image_byte_code")
        if image_byte_code == 'false':
            image_byte_code = False
            pass
        try:
            image_byte_code1 = request.POST.get("image_byte_code")
            image_byte_code = image_byte_code1.split(',')[1]
        except:
            pass
        attached_file_name = False
        try:
            attached_file_name1 = request.FILES['employee_attached_file']
            print("attached_file_name1:::::",str(attached_file_name1))
            attached_file_name = str(attached_file_name1)
        except:
            pass
        employee_name1 = request.POST.get("employee_name1",False)
        leave_type_nm = request.POST.get("leave_type_nm",False)
        user_auth_id = request.user.id
        data_employee = User_Management.objects.get(auth_user=user_auth_id)
        employee_name = request.POST.get("employee_name",False)
        print("new employee_name::::",str(employee_name))
        print("new employee id:::",str(employee_name1))
        employee_email = request.POST.get("employee_email",False)
        employee_number = request.POST.get("employee_number",False)
        employee_leave_type = request.POST.get("employee_leave_type",False)
        if  employee_leave_type == 'no':
            messages.warning(request,str("Please Select Leave Type !!!"))
            return redirect("leave_management")
        employee_leave_from_date = request.POST.get("employee_leave_from_date",False)
        employee_leave_to_date = request.POST.get("employee_leave_to_date",False)
        employee_available_leave = request.POST.get("employee_available_leave",False)
        employee_leave_reason = request.POST.get("employee_leave_reason",False)
        employee_total_days = request.POST.get("employee_total_days",False)
        employee_leave_replacer = request.POST.get("employee_leave_replacer",False)
        employee_alternative_contcat_no = request.POST.get("employee_alternative_contcat_no",False)
        request_unit_half= request.POST.get("request_unit_half",False)
        if request_unit_half == 'false':
            request_unit_half = False
        print("request_unit_half111111111111:::::::::::;",request_unit_half)
        print(type(request_unit_half))
        absence_status = request.POST.get("absence_status",False)
        absence_category = request.POST.get("absence_category",False)
        if request_unit_half == "Half day":
            employee_leave_to_date = employee_leave_from_date
            pass
        request_date_from_period = request.POST.get("request_date_from_period",False)
        if employee_leave_replacer == 'null':
            employee_leave_replacer =int(0)
        leave_apply_url = api_domain+"api/post_leave"
        print("")
        payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "leave_type": int(employee_leave_type),
                "from_date": employee_leave_from_date,
                "to_date": employee_leave_to_date,
                "total_days": employee_total_days,
                "reason": employee_leave_reason,
                "alternative_contact_number": employee_alternative_contcat_no,
                "replacer": employee_leave_replacer,
                "holiday_type": "employee",
                "employee_id": int(employee_name),
                'request_unit_half':request_unit_half,
                'request_date_from_period':request_date_from_period,
                'absence_status':absence_status,
                'absence_category':absence_category,
                'binary_attachment':image_byte_code,
                'binary_attachment_name':attached_file_name
            }
        })
        odoo_token_data = odoo_api_request_token.objects.get(status="True")
        headers = {
            'api_key': odoo_token_data.token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        print("responseeeeeeeeeeeeeeeeeeeeeeeeee")
        response1 = requests.request("POST", leave_apply_url, headers=headers, data=payload)
        print("result::::",str(response1))
        response12 = response1.json()['result']
        print("response12::::",str(response12))
        l1 = response12['result']
        responsible_for_approval = ""
        try:
            responsible_for_approval = l1['responsible_for_approval']
        except:
            pass
        if response12['message'] == "error":
            message = response12['result']
            mes1 = response12['result']
            m1 = mes1[:mes1.index("\n")]
            data = []
            data = {
                'message':str(m1),
                'submit_message':"error"
            }
            print("kkkllll")
            return JsonResponse(data,safe=False)
            messages.warning(request,str(m1))
            return redirect("leave_management")
        elif response12['message'] == "success":
            from datetime import date
            today = date.today()
            message = response12['result']
            mes1 = "Your Leave from "+str(employee_leave_from_date)+" to "+str(employee_leave_to_date)+" has been submitted"
            r1 = response12['result']
            leave_id = r1['leave_id']
            leave_state = r1['state']
            leave_notification = odoo_notification(
                notification_type="leave_type",
                message = "The leave you applied on ",
                mapping_id = int(leave_id),
                requested_from_dt = employee_leave_from_date,
                requested_to_dt = employee_leave_to_date,
                read_status = 0,
                status = leave_state,
                auth_user_id = request.user,
                leave_type_name=leave_type_nm,
                leave_apply_user_name = employee_name1,
               description =employee_leave_reason,
               category = "notification"
            )
            leave_notification.save()
            check_data=""
            second_user_id = 0
            submit_status = Leave_Status_details(
                leave_mapping_id =int(leave_id),
                user_name  = employee_name1,
                status = "Submit",
                dt = today,
                auth_user = request.user
            )
            submit_status.save()
            print("nextapproval::::::",str(responsible_for_approval))
            
            try:
                check_data = User_company_details.objects.get(odoo_id=int(responsible_for_approval))
                user__id = check_data.auth_user_id
                message = "one leave request from " +employee_name1
                try:
                    send_push_notification(user__id,employee_name1)
                except:
                    pass
                print("check_data::::",str(check_data.auth_user_id.id))
                second_user_id = check_data.auth_user_id.id
               
                approval_notification =  odoo_notification(
                    notification_type="leave_approve_request",
                    message = "leave_approve_request",
                    mapping_id = int(leave_id),
                    requested_from_dt = employee_leave_from_date,
                    requested_to_dt = employee_leave_to_date,
                    read_status = 0,
                    status = leave_state,
                    auth_user_id = check_data.auth_user_id,
                    leave_type_name=leave_type_nm,
                    leave_apply_user_name = employee_name1,
                    description =employee_leave_reason,
                    current_leave_status = "confirm",
                    category = "activities"
                )
                approval_notification.save()
                submit_status1 = Leave_Status_details(
                            leave_mapping_id =int(leave_id),
                            user_name  = check_data.employee_name,
                            status = "Pending",
                        dt = today,
                        auth_user = check_data.auth_user
                )
                submit_status1.save() 
            except:
                pass
            print("ttttttaaat:::",str(second_user_id))
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notification_broadcast2",
                {      
                    'type': 'send_notification',
                    'message':{
                        "message":str("Leave Approve Request"),
                        "dt":str(employee_leave_from_date),
                        "status":str(leave_state),
                        "requested_date_from":str(employee_leave_from_date),
                        "requested_date_to":str(employee_leave_to_date),
                        "send_user_id":second_user_id,
                        "category":"activities"
                    }
                }
            )
            data = []
            data = {
                'message':str(mes1),
                'submit_message':'success'
            }
            print("kkkllll")
            try:
                leave_draft_id = request.POST.get("leave_draft_id",False)
                update_status = User_leave_draf_history.objects.filter(id=leave_draft_id).update(status="submit")
            except:
                pass
            messages.success(request,str(mes1))
            return JsonResponse(data,safe=False)
            return redirect("leave_management")    



@login_required(login_url='/index')
def view_all_notification(request):
    type = request.GET.get("type",False)
    print("type:::",str(type))
    if type == "notification":
         update_noti = odoo_notification.objects.filter(read_status=0,auth_user_id=request.user,category="notification").update(
            read_status=1
        )

    if type == "activities":
        notifictaion = odoo_notification.objects.filter(auth_user_id=request.user,category="activities",read_status=0).order_by('-id')
    else:
        notifictaion = odoo_notification.objects.filter(auth_user_id=request.user,category="notification").order_by('-id')
        notifictaion = notifictaion[0:10]



    
    # update_noti = odoo_notification.objects.filter(read_status=0,auth_user_id=request.user).update(
    #     read_status=1
    # )
    context = {
        "notifictaion":notifictaion,
        'type':type
    }
    return render(request,'super_admin/view_all_notification.html',context)



from rest_framework.decorators import api_view
@api_view(['POST'])
def leave_status_update_api(request):
    if request.method == "POST":
        print("-------------createdapiiiiiii")
        leave_id = request.POST.get("leave_id",False)
        state = request.POST.get("state",False)
        updated_data = odoo_notification.objects.filter( mapping_id = int(leave_id),notification_type="leave_type").update(status=state,read_status=0)
        data = {
            'message':"success"
        }
        data_send = odoo_notification.objects.get(mapping_id= int(leave_id),notification_type="leave_type")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notification_broadcast2",
            {
                'type': 'send_notification',
                'message':{
                    "message":str(data_send.message),
                    "dt":str(data_send.dt),
                    "status":str(state),
                    "requested_date_from":str(data_send.requested_from_dt),
                    "requested_date_to":str(data_send.requested_to_dt),
                    "send_user_id":data_send.auth_user_id.id
                }
            }
        )
        print("notifiiiiiiiiii")


     
        return JsonResponse(data,safe=False)






def test_r1(request):
    return render(request,'super_admin/index1.html',{
        'room_name': "broadcast",
        
        
    })



def test_r2(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast2",
        {
            'type': 'send_notification',
            'message':{
                "message":"hellooooo how are you",
                "dt":"29-03-2022",
                "status":"approved",
                "requested_date_from":"29-03-2022",
                "requested_date_to":"30-03-2022",
                "send_user_id":5
            }
        }
    )
     
    return HttpResponse("Done")


@login_required(login_url='/index')
def view_leave_more_details(request):
    id = request.GET.get("id",False)
    leave_more_details_url = api_domain+"api/get_leave_details"
    payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "leave_id" : int(id)  
            }
    })
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    headers = {
        'api_key': odoo_token_data.token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    response1 = requests.request("GET", leave_more_details_url, headers=headers, data=payload)
    response12 = response1.json()['result']
    r1 = response12['result'][0]
    attach = ""
    type1 = ""
    name = ""
    try:
        attach = r1['attachments'][0]['datas']
        type1 = r1['attachments'][0]['mimetype']
        name = r1['attachments'][0]['name']
    except:
        pass
    df = r1['leave_logs']
    emp_name = ""
    try:
        data_emp = User_Management.objects.get(auth_user=request.user)
        emp_name = data_emp.employee_name
    except :
        pass
    approve_button_status = ""
    try:
        approval_instance = odoo_notification.objects.get(mapping_id=id,auth_user_id=request.user,notification_type="leave_approve_request",status="Pending")
        approve_button_status = "yes"
    except:
        approve_button_status ="no"
        pass
    select_employee_api = ""
    try:
        odoo_token_data = odoo_api_request_token.objects.get(status="True")
        odoo_token = odoo_token_data.token
        employee_data_url =api_domain+"api/get_employees"
        user_data = User_company_details.objects.all()
        list_data = list(user_data.values_list('odoo_id',flat=True))
        print("listaaaa_data:::",str(list_data))

        user_data1 = User_Management.objects.get(auth_user=request.user)
        print("user_data1:::",str(user_data1.employee_company_id))
        payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                 "reassign" : "True",
            "employee_ids": list_data,
            'company_id':user_data1.employee_company_id
            }
        })
        headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        select_employee_api1 = requests.request("GET", employee_data_url, headers=headers, data=payload)
        response_result = select_employee_api1.json()['result']
        select_employee_api = response_result['result']
    except:
        pass
    data_leave_status = Leave_Status_details.objects.filter(leave_mapping_id=id)
    context = {
        'r1':r1,
        'emp_name':emp_name,
        'approve_button_status':approve_button_status,
        'id':id,
        'select_employee_api':select_employee_api,
        'data_leave_status':data_leave_status,
        'history_action':df,
        'attach':attach,
        'type1':type1,
        'name':name
    }
    return render(request,'super_admin/view_leave_more_details.html',context)


def get_selected_employee_entitlement_balance(request):
    employee_id = request.GET.get("employee_id",False)
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    employee_data_url =api_domain+"api/get_employee"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id": int(employee_id)
        }
    })
    headers = {
        'api_key': odoo_token_data.token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    response1  = requests.request("GET", employee_data_url, headers=headers, data=payload).json()
    response12 =response1['result']
    response = response12['result'][0]
    employee_name1 = response['name']
    emp_registration_id = response['registration_number']

    data = []
    data = {
        'employee_reg_number':emp_registration_id,
        'employee_name1':employee_name1
    }
    return JsonResponse(data,safe=False)
  
    return render(request,'super_admin/get_selected_employee_entitlement_balance.html',{'entitlement_balances_response':'','emp_registration_id':emp_registration_id,'employee_name1':employee_name1})





def get_child_based_leave_history(request):
    employee_id = request.GET.get("employee_id",False)
   
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    leave_history_response = ""
    try:
        leave_history_response_url = api_domain+"api/get_leave_history"
        leave_history_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id": int(employee_id)
            }
        })
        leave_history_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers, data=leave_history_payload).json()
       
        
        leave_history_response12  = leave_history_response1['result']
        leave_history_response = leave_history_response12['result']
        
        

    except:
        pass
    return render(request,'super_admin/get_child_based_leave_history.html',{'leave_history_response':leave_history_response})



def testchart(request):
    import calendar
    import datetime
    now = datetime.datetime.now()
   
    days = calendar.monthrange(now.year, now.month)[1]
 
    month_num = str(now.month)
    datetime_object = datetime.datetime.strptime(month_num, "%m")

    month_name = datetime_object.strftime("%b")


    full_month_name = datetime_object.strftime("%B")
  

    employee_data = User_Management.objects.get(auth_user=request.user)

    import datetime, calendar
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]


  

    context = {
        'full_month_name':full_month_name,
        'days':days,
        'employee_data_name':employee_data.employee_name,
        'ays':ays
    }

    return render(request,'super_admin/testchart.html',context)




def user_leave_gantt_chart(request):
    import calendar
    import datetime
    now = datetime.datetime.now()

    days = calendar.monthrange(now.year, now.month)[1]
  
    month_num = str(now.month)
    datetime_object = datetime.datetime.strptime(month_num, "%m")

    month_name = datetime_object.strftime("%b")
  

    full_month_name = datetime_object.strftime("%B")


    employee_data = User_Management.objects.get(auth_user=request.user)

    import datetime, calendar
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]

    year = now.year
    month = now.month


    get_chile_response = ""
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    send_data = str(year)+"-"+str(month)
    try:
        get_chile_response_response_url = api_domain+"api/get_childs"
        get_chile_response_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id": int(employee_data.odoo_id),
               
                'leave_gantt':"True",
                "date" : send_data
            }
        })
        get_chile_response_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        get_chile_response1 = requests.request("GET", get_chile_response_response_url, headers=get_chile_response_headers, data=get_chile_response_payload).json()
        
        
        get_chile_response112  = get_chile_response1['result']
        get_chile_response = get_chile_response112['result']
        
       
        

    except:
        pass




    



    

    context = {
        'full_month_name':month_name,
        'days':days,
        'employee_data_name':employee_data.employee_name,
        'ays':ays,
        'year':year,
        'month':month,
        'get_chile_response':get_chile_response,
        'send_data':send_data
    }

    return render(request,'super_admin/user_leave_gantt_chart.html',context)



def user_leave_gantt_chart_next_month_action(request):

    from datetime import date
    y = request.GET.get("year",False)
    m = request.GET.get("month",False)
    try:
        df = date(int(y),int(m)+1,1)
    except:
        df = date(int(y)+1,int(1),1)
    new_month = df.month
    new_year = df.year

    
    import calendar
    import datetime
    
    days = calendar.monthrange(int(new_year), int(new_month))[1]
   

    month_num = str(m)
    datetime_object = datetime.datetime.strptime(str(new_month), "%m")

    month_name = datetime_object.strftime("%b")


    full_month_name = datetime_object.strftime("%B")
   
    employee_data = User_Management.objects.get(auth_user=request.user)
    import datetime, calendar
    year = new_year
    month = new_month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]

    send_data = str(year)+"-"+str(month)
    get_chile_response = ""
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
   
    try:
        get_chile_response_response_url = api_domain+"api/get_childs"
        get_chile_response_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id": int(employee_data.odoo_id),
                "exclud_parent" : "True",
                'leave_gantt':"True",
                "date" : send_data
            }
        })
        get_chile_response_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        get_chile_response1 = requests.request("GET", get_chile_response_response_url, headers=get_chile_response_headers, data=get_chile_response_payload).json()
        
        
        get_chile_response112  = get_chile_response1['result']
        get_chile_response = get_chile_response112['result']
   
       
        

    except:
        pass

    count1 = 0


   
    context = {
        'full_month_name':month_name,
        'days':days,
        'employee_data_name':employee_data.employee_name,
        'ays':ays,
        'year':year,
        'month':month,
        'send_data':send_data,
        'get_chile_response':get_chile_response,
        'count1':0
    }

    return render(request,'super_admin/user_leave_gantt_chart1.html',context)



def user_leave_gantt_chart_prev_month_action(request):

    from datetime import date
    y = request.GET.get("year",False)
    m = request.GET.get("month",False)
    try:
        df = date(int(y),int(m)-1,1)
    except:
        if int(m)==12:

            df = date(int(y)-1,int(1),1)
        elif int(m) == 1:
            df = date(int(y)-1,int(12),1)

        else:
            df = date(int(y)-1,int(1),1)

    new_month = df.month
    new_year = df.year
   
    
    import calendar
    import datetime
    
    days = calendar.monthrange(int(new_year), int(new_month))[1]


    month_num = str(m)
    datetime_object = datetime.datetime.strptime(str(new_month), "%m")

    month_name = datetime_object.strftime("%b")
  

    full_month_name = datetime_object.strftime("%B")
    
    employee_data = User_Management.objects.get(auth_user=request.user)
    import datetime, calendar
    year = new_year
    month = new_month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]
   
    send_data = str(year)+"-"+str(month)
    get_chile_response = ""
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
   
    try:
        get_chile_response_response_url = api_domain+"api/get_childs"
        get_chile_response_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id": int(employee_data.odoo_id),
                "exclud_parent" : "True",
                'leave_gantt':"True",
                "date" : send_data
            }
        })
        get_chile_response_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        get_chile_response1 = requests.request("GET", get_chile_response_response_url, headers=get_chile_response_headers, data=get_chile_response_payload).json()
        
        
        get_chile_response112  = get_chile_response1['result']
        get_chile_response = get_chile_response112['result']
       
       
        

    except:
        pass

    context = {
        'full_month_name':month_name,
        'days':days,
        'employee_data_name':employee_data.employee_name,
        'ays':ays,
        'year':year,
        'month':month,
        'get_chile_response':get_chile_response,
        'send_data':send_data
    }

    return render(request,'super_admin/user_leave_gantt_chart1.html',context)






def calendar(request):
    user_auth_id = request.user.id
    print("user_auth_id::::", str(user_auth_id))
    odoo_id = 0
    try:

        odoo_data = User_Management.objects.get(auth_user=user_auth_id)
        odoo_id = odoo_data.odoo_id

    except:
        pass
    print("odoo_id::::::", str(odoo_id))

    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token

    context = {

    }

    return render(request, 'super_admin/calendar.html', context)
    # return render(request, 'super_admin/calendar.html')



def depended(request):
    dt=request.GET.get('date_emp')
    print("dt:::::::::::::::::::::",dt)
    print(type(dt))
    from datetime import datetime
    dd=datetime.fromisoformat(dt[:-1])
    date = dd.date()
    date_month=str(date.year)+'-'+str(date.month)
    print("dd:::::::::::::::::::::", date_month)
    print(type(date))
    # datetime.datetime(2020, 1, 6, 0, 0, tzinfo=datetime.timezone.utc)
    user_auth_id = request.user.id
    print("user_auth_id::::", str(user_auth_id))
    odoo_id = 0
    try:

        odoo_data = User_Management.objects.get(auth_user=user_auth_id)
        odoo_id = odoo_data.odoo_id

    except:
        pass
    print("odoo_id::::::", str(odoo_id))

    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token

    child_response = ""
    try:
        child_response_url = api_domain + "api/get_childs"
        child_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {

                "employee_id" : odoo_id,
                "date" : date_month,
                "leave_gantt" : "True",
                "leave_type_include" : "True"
            }
        })
        child_header = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        child_response1 = requests.request("GET", child_response_url, headers=child_header, data=child_payload).json()
        child_response12 = child_response1['result']
        child_response = child_response12['result']
    except:
        pass
    # list1 = [1, 2, 3, 4, 4, 4]
    # print(list(set(list1)))
    print("child_response::::::::",child_response)
   
    
    leave_type = []
    for i in child_response:
        print("leave_type:sssssssssss:::qq111:::",i['leave_types'])

        for j in i['leave_types']:
            print("j111ssssssss:::::",str(j))
            
            leave_type.append({

                'id': j[0],
                'name': j[1]
            })
            seen = set()
            new_l = []
            for d in leave_type:
                t = tuple(d.items())
                if t not in seen:
                    seen.add(t)
                    new_l.append(d)

            print ("::::::::::::::::::::::::jiya",new_l)

    
    print("leave_type1112qqq222:::",str(leave_type))
   
    context = {

        'child_response': child_response,
        'leave_list_data':new_l
        # 'new_list': child_response['leave_type'],
        # 'li':li
    }

    return render(request, 'super_admin/depended.html', context)



def img(request):
    if request.method == "POST":
        
        n1 = request.POST.getlist('n1[]')
       
        for i in range(len(n1)):
           
            save = test.objects.create(
                img_path=n1[i]
            )
       
        files = request.FILES.getlist('files[]')
      
    else:
        test1 = test.objects.all()
        
        return render(request,'super_admin/img.html',{'test1':test})




def view_notification_table(request):

    type = request.GET.get("type",False)
    print("type:::",str(type))
    if type == "notification":
         update_noti = odoo_notification.objects.filter(read_status=0,auth_user_id=request.user,category="notification").update(
            read_status=1
        )

    if type == "activities":
        notifictaion = odoo_notification.objects.filter(auth_user_id=request.user,category="activities",read_status=0).order_by('-id')
    else:
        notifictaion = odoo_notification.objects.filter(auth_user_id=request.user,category="notification").order_by('-id')


    context = {
        "notifictaion":notifictaion,
        'type':type
    }
    return render(request,'super_admin/view_notification_table.html',context)




def leave_approve_action(request):
    if request.method == "POST":
        print("hhhh")
        leave_mapping_id = request.POST.get("leave_mapping_id",False)
        leave_status = request.POST.get("leave_status",False)
        login_user_data = User_Management.objects.get(auth_user=request.user)
        odoo_employee_id = login_user_data.odoo_id
        odoo_token_data = odoo_api_request_token.objects.get(status="True")
        odoo_token = odoo_token_data.token

        print("leave_mapping_id:::",str(leave_mapping_id))
        print("leave_status:::::",str(leave_status))
        print("login_user_data::",str(login_user_data))
        print("odoo_employee_id:::",str(odoo_employee_id))
        print("odoo_token:::",str(odoo_token))
        approval_api_url = api_domain+"api/approve_leave_req"
        approval_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "leave_id" : leave_mapping_id,
                "employee_id" : int(odoo_employee_id),
                "state":leave_status
            }
        })
        approval_header = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        approval_response = requests.request("GET", approval_api_url, headers=approval_header,
                                                   data=approval_payload).json()
        response = approval_response['result']
        print("response::::",str(response))
        if response['message'] == "success":
            response_result = response['result']
            leave_id = response_result['leave_id']
            leave__result_status = response_result['status']
            responsible_for_approval = response_result['responsible_for_approval']
            data_update_approve_status = odoo_notification.objects.filter(mapping_id=leave_id,auth_user_id=request.user,notification_type="leave_approve_request",status="Pending").update(status="approve",read_status=1)
            data_update_requested_user_status = odoo_notification.objects.filter(mapping_id=leave_id,notification_type="leave_type").update(status=leave__result_status,read_status=0)
            try:
                send_request = odoo_notification.objects.get(mapping_id=leave_id,notification_type="leave_type")
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "notification_broadcast2",
                    {       
                        'type': 'send_notification',
                        'message':{
                            "message":str("Leave Approve Request"),
                            "dt":str(send_request.dt),
                            "status":str(leave__result_status),
                            "requested_date_from":str(send_request.requested_from_dt),
                            "requested_date_to":str(send_request.requested_to_dt),
                            "send_user_id":send_request.auth_user_id.id,
                            "category":"notification"
                        }
                    }
                )
            except:
                pass
            print("new methodddd")
            print("responsible_for_approval::::::",str(responsible_for_approval))
            print("leave__result_status::::::",str(leave__result_status))
            
            # updated_leave_status = Leave_Status_details.objects.filter(auth_user=request.user).update(status="Approved")
            if leave__result_status == "validate":
                pass
            else:
            
                try:
                    next_approve_user_data = User_company_details.objects.get(odoo_id=responsible_for_approval)
                    try:
                        leave_data = odoo_notification.objects.get(mapping_id=leave_id,notification_type="leave_type")
                    except:
                        leave_data = odoo_notification.objects.get(mapping_id=leave_id,auth_user_id=request.user,notification_type="leave_approve_request",status="approve")
                    
                    print("-------------------next approveeeeeeeeeeeeeeeeeee----------------------")
                    next_approval_notification = odoo_notification.objects.create(
                        notification_type="leave_approve_request",
                        message="leave request",
                        mapping_id = leave_id,
                        requested_from_dt = leave_data.requested_from_dt,
                        requested_to_dt = leave_data.requested_to_dt,
                        read_status = 0,
                        status = "Pending",
                        auth_user_id_id = next_approve_user_data.auth_user_id.id,
                        leave_type_name = leave_data.leave_type_name,
                        leave_apply_user_name = leave_data.leave_apply_user_name,
                        description = "null",
                        current_leave_status = leave__result_status,
                        category = "activities"
                    )
                    
                    from datetime import date

                    today = date.today()
                   
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "notification_broadcast2",
                        {       
                            'type': 'send_notification',
                            'message':{
                            "message":str("Leave Approve Request"),
                            "dt":str(send_request.dt),
                            "status":str(leave__result_status),
                            "requested_date_from":str(send_request.requested_from_dt),
                            "requested_date_to":str(send_request.requested_to_dt),
                            "send_user_id":next_approve_user_data.auth_user_id.id,
                            "category":"activities"
                        }
                    }
                    )
                except:
                    pass
            

            print("--------------approveddddddddddddddddddddddddddd")

            messages.success(request,str("approved success"))
            return redirect(request.META['HTTP_REFERER']) 
        else:
            response_result = response['result']
            res1 = response_result.split(":")
            
            print("response_result::::::",str(res1[0]))
            messages.warning(request,str(res1[0]))
            return redirect(request.META['HTTP_REFERER']) 
            pass





def reject_leave_request_action(request):
    if request.method == "POST":
        print("heyyyyyyyyyyyyyyyyyyyyy1")
        leave_mapping_id = request.POST.get("leave_mapping_id",False)
        leave_status = request.POST.get("leave_status",False)
        note = request.POST.get("note",False)
        login_user_data = User_Management.objects.get(auth_user=request.user)
        odoo_employee_id = login_user_data.odoo_id
        odoo_token_data = odoo_api_request_token.objects.get(status="True")
        odoo_token = odoo_token_data.token
        reject_api_url = api_domain+"api/refuse_leave_req"
        reject_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "leave_id" : leave_mapping_id,
                "employee_id" : int(odoo_employee_id),
                 "refuse_reason" : note
            }
        })
        reject_header = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        reject_response = requests.request("GET", reject_api_url, headers=reject_header,
                                                   data=reject_payload).json()
        print("reject_response23:::")
        print(reject_response)
        response = reject_response['result']
        if response['message'] == "success":
            print("rejecttttttttttttt::")
            print("heyyyyyyyyyyyyyyyyyyyyy12")

            response_result = response['result']
            leave_id = response_result['leave_id']
            leave__result_status = response_result['status']

            update_leave_status = Leave_Status_details.objects.filter(auth_user=request.user,leave_mapping_id=leave_id).update(status="Rjected",note=note)

            
            # responsible_for_approval = response_result['responsible_for_approval']
            data_update_approve_status = odoo_notification.objects.filter(mapping_id=leave_id,auth_user_id=request.user,notification_type="leave_approve_request",status="Pending").update(status="reject",read_status=1)
            data_update_requested_user_status = odoo_notification.objects.filter(mapping_id=leave_id,notification_type="leave_type").update(status=leave__result_status,read_status=0)
            
        messages.success(request,str("Reject success"))
        return redirect(request.META['HTTP_REFERER']) 
        pass



def leave_reassign_action(request):
    if request.method == "POST":
        leave_mapping_id = request.POST.get("leave_mapping_id",False)
        leave_status = request.POST.get("leave_status",False)
        selected_employee_id = request.POST.get("selected_employee_id",False)
        login_user_data = User_Management.objects.get(auth_user=request.user)
        odoo_employee_id = login_user_data.odoo_id
        odoo_token_data = odoo_api_request_token.objects.get(status="True")
        odoo_token = odoo_token_data.token
        reassign_api_url = api_domain+"api/ressign_leave_req"
        reassign_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "leave_id" : leave_mapping_id,
                "employee_id" : int(odoo_employee_id),
                "next_responsibe_employee_id" : int(selected_employee_id)
            }
        })
        print("reassign_payload::::::;;;;",reassign_payload)
        reassign_header = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        reassign_response = requests.request("GET", reassign_api_url, headers=reassign_header,
                                                   data=reassign_payload).json()
        print("reassign_response:::" ,reassign_response)
        response = reassign_response['result']
        if response['message'] == "success":
            print("reassignnnnnnnnnned::")
            response_result = response['result']
            leave_id = response_result['leave_id']
            leave__result_status = response_result['status']
            # responsible_for_approval = response_result['responsible_for_approval']
            data_update_approve_status = odoo_notification.objects.filter(mapping_id=leave_id,auth_user_id=request.user,notification_type="leave_approve_request",status="Pending").update(status="reassign",read_status=1)
            data_update_requested_user_status = odoo_notification.objects.filter(mapping_id=leave_id,notification_type="leave_type").update(status=leave__result_status,read_status=0)
            next_approve_user_data = ""
            try:
                next_approve_user_data = User_company_details.objects.get(odoo_id=int(selected_employee_id))
            except:
                pass
            try:
                leave_data = odoo_notification.objects.get(mapping_id=leave_id,notification_type="leave_type")
            except:
                leave_data = odoo_notification.objects.get(mapping_id=leave_id,auth_user_id=request.user,notification_type="leave_approve_request")

            try:
                next_approval_notification = odoo_notification(
                    notification_type="leave_approve_request",
                    message="leave request",
                    mapping_id = leave_id,
                    requested_from_dt = leave_data.requested_from_dt,
                    requested_to_dt = leave_data.requested_to_dt,
                    read_status = 0,
                    status = "Pending",
                    auth_user_id_id = next_approve_user_data.auth_user_id.id,
                    leave_type_name = leave_data.leave_type_name,
                    leave_apply_user_name = leave_data.leave_apply_user_name,
                    description = "null",
                    current_leave_status = leave__result_status,
                    category = "activities"
                )
                next_approval_notification.save()
            except:
                pass 
            try:
                leave_status_update = Leave_Status_details.objects.filter(auth_user=request.user).update(status="Reassigning",note=next_approve_user_data.user_id.employee_name)
            except:
                pass
            from datetime import date
            today = date.today()
            try:
                add_leave_status = Leave_Status_details.objects.create(
                    leave_mapping_id = int(leave_id),
                    user_name = next_approve_user_data.user_id.employee_name,
                    auth_user = next_approve_user_data.user_id.auth_user,
                    dt = today,
                    status = "Pending"
                )
            except:
                pass
        messages.success(request,str("Reassign success"))
        return redirect(request.META['HTTP_REFERER']) 
        pass




from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def user_fcmtoken_save(request):

    token=request.POST.get("token")
    print('tokennnnnnnnnnnnnnnnn:',token)
    try:

        user_fcm=user_fcm_token.objects.get(user=request.user)
        print('userrrrrrrrr',user_fcm)
        user_fcm.fcm_token=token
        user_fcm.save()
        return HttpResponse("True")
    except user_fcm_token.DoesNotExist:
        data_save = user_fcm_token(
            user=request.user,
            fcm_token = token
        )
        data_save.save()
        return HttpResponse("True")



def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyBUzBd7jlI4_xOOWk1Z21KGGeDmUogUL7s",' \
         '        authDomain: "tss-leave-15620.firebaseapp.com",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '       projectId: "tss-leave-15620",' \
         '         storageBucket: "tss-leave-15620.appspot.com",' \
         '        messagingSenderId: "644297127885",' \
         '        appId: "1:644297127885:web:02256dc071fd129fb33684",' \
         '         measurementId: "G-8NFZMH0NY4"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")




def loader(request):
    return render(request,'super_admin/loader.html')






# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'tss_database',
#         'USER': 'tss',
#         'PASSWORD': '2021@tss',
#         'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#     }
# }







from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
class leave_create_api(APIView):
    permission_classes = (IsAuthenticated,)

    print("----------------createddddddddddddddddddddddd")
    
    def post(self, request, format=None):
        data = request.data
        leave_request_user_id = data['leave_request_user_id']
        leave_mapping_id = data['leave_mapping_id']
        leave_from_dt = data['leave_from_dt']
        leave_to_dt = data['leave_to_dt']
        print("leave_to_dt:::",str(leave_to_dt))
        leave_type = data['leave_type']
        leave_request_user_name = data['leave_request_user_name']
        leave_reason = data['leave_reason']
        responsible_for_approval_user_id = data['responsible_for_approval_user_id']
        leave_state = data['leave_state']
        print("leave_request_user_id:::",str(leave_request_user_id))
        print("responsible_for_approval_user_id::::",str(responsible_for_approval_user_id))
        from datetime import datetime
        dt_obj = datetime.fromtimestamp(leave_to_dt)
        dt_obj1 = datetime.fromtimestamp(leave_from_dt)
        
        try:
            apply_user_exist_instance = User_Management.objects.get(odoo_id=int(leave_request_user_id))
            apply_user_exist_instance_auth = apply_user_exist_instance.auth_user
            leave_notification = odoo_notification(
                notification_type="leave_type",
                message = "The leave you applied on ",
                mapping_id = int(leave_mapping_id),
                requested_from_dt =  dt_obj1.date(),
                requested_to_dt = dt_obj.date(),
                read_status = 0,
                status = leave_state,
                auth_user_id = apply_user_exist_instance_auth,
                leave_type_name=leave_type,
                leave_apply_user_name = leave_request_user_name,
               description =leave_reason,
               category = "notification"
            )
            leave_notification.save()
        except User_Management.DoesNotExist:
            pass
        
       
        next_approval = User_Management.objects.get(odoo_id=int(responsible_for_approval_user_id))
        user__id = next_approval.auth_user
        message = "one leave request from " +leave_request_user_name
        try:

            send_push_notification(user__id,leave_request_user_name)
        except:
            pass
        second_user_id = next_approval.auth_user.id
        approval_notification =  odoo_notification(
                notification_type="leave_approve_request",
                message = "leave_approve_request",
                mapping_id = int(leave_mapping_id),
                requested_from_dt =  dt_obj1.date(),
                requested_to_dt =  dt_obj.date(),
                read_status = 0,
                status = "Pending",
                auth_user_id = next_approval.auth_user,
                leave_type_name=leave_type,
                leave_apply_user_name = leave_request_user_name,
                description =leave_reason,
                current_leave_status = "confirm",
                category = "activities",
                
        )
        approval_notification.save()
       
        content = {
           "message":"success"
        }
        return Response(content)



class odoo_leave_status_update_api(APIView):

    permission_classes = (IsAuthenticated,)
    print("----------------createdddddddddddddddddddddddstatusssss")
    
    def post(self, request, format=None):
        print("0000")
        data = request.data
        print("data::",str(data))
        leave_id = data['leave_id']
        state = data['state']
        responsible_for_approval_user_id = data['responsible_for_approval_user_id']
        current_leave_state = data['state']
        login_user_id = data['activity_done_by']
        print("login_user_id::::",str(login_user_id))

        try:
            activity_done_by_user = User_Management.objects.get(odoo_id=login_user_id)
            odoo_notification.objects.filter(mapping_id=leave_id,auth_user_id=activity_done_by_user.auth_user,notification_type="leave_approve_request",status="Pending").update(status="approve",read_status=1)
        except:
            pass



        try:
            updated_data = odoo_notification.objects.filter( mapping_id = int(leave_id),notification_type="leave_type").update(status=state,read_status=0)
        except:
            pass
        data = {
            'message':"success"
        }
        try:
            data_send = odoo_notification.objects.get(mapping_id= int(leave_id),notification_type="leave_type")
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notification_broadcast2",
                {
                'type': 'send_notification',
                'message':{
                    "message":str(data_send.message),
                    "dt":str(data_send.dt),
                    "status":str(state),
                    "requested_date_from":str(data_send.requested_from_dt),
                    "requested_date_to":str(data_send.requested_to_dt),
                    "send_user_id":data_send.auth_user_id.id
                }
                }
            )
        except:
            pass

        try:
            next_approve_user_data = User_Management.objects.get(odoo_id=responsible_for_approval_user_id)
            try:
                leave_data = odoo_notification.objects.get(mapping_id=leave_id,notification_type="leave_type")
            except:
                leave_data = odoo_notification.objects.get(mapping_id=leave_id,auth_user_id=activity_done_by_user.auth_user,notification_type="leave_approve_request")
            next_approval_notification = odoo_notification(
                notification_type="leave_approve_request",
                message="leave request",
                mapping_id = leave_id,
                requested_from_dt = leave_data.requested_from_dt,
                requested_to_dt = leave_data.requested_to_dt,
                read_status = 0,
                status = "Pending",
                auth_user_id_id = next_approve_user_data.auth_user.id,
                leave_type_name = leave_data.leave_type_name,
                leave_apply_user_name = leave_data.leave_apply_user_name,
                description = "null",
                current_leave_status = current_leave_state,
                category = "activities"
            )
            next_approval_notification.save()
            
        except User_Management.DoesNotExist:
            pass
        return Response(data)









def leave_calendar(request):
    user_auth_id = request.user.id
    odoo_id = 0
    try:

        odoo_data = User_Management.objects.get(auth_user=user_auth_id)
        odoo_id = odoo_data.odoo_id

    except:
        pass
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token


    return render(request, 'super_admin/leave_calendar.html')



def event_depended(request):
    event_id = request.GET.get('event_id')
    leave_more_details_url = api_domain + "api/get_leave_details"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "leave_id": int(event_id)

        }
    })
    odoo_token_data = odoo_api_request_token.objects.get(status="True")

    headers = {
        'api_key': odoo_token_data.token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    response1 = requests.request("GET", leave_more_details_url, headers=headers, data=payload)
    response12 = response1.json()['result']
    r1 = response12['result'][0]
    emp_name = ""
    try:
        data_emp = User_Management.objects.get(auth_user=request.user)
        emp_name = data_emp.employee_name
    except:
        pass
    context = {
        'r1': r1,
        'emp_name': emp_name
    }

    return render(request, 'super_admin/event_depended.html',context)


def all_events(request):
    user_auth_id = request.user.id
    odoo_id = 0
    try:

        odoo_data = User_Management.objects.get(auth_user=user_auth_id)
        odoo_id = odoo_data.odoo_id

    except:
        pass
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    leave_history_response = ""
    try:
        leave_history_response_url = api_domain + "api/get_leave_history_calender"
        leave_history_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {

            "employee_id" : odoo_id,
            "all": "True",
            "start_date" : "2022-07-01",
            "end_date" : "2022-07-31",
            }
        })
        leave_history_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers,
                                                   data=leave_history_payload).json()


        leave_history_response12 = leave_history_response1['result']
        leave_history_response = leave_history_response12['result']


    except:
        pass
    out = []
    for event in leave_history_response:
        from datetime import datetime
        df = datetime.fromisoformat(event['date_to'])
        from datetime import timedelta
        date_time_obj = df+timedelta(days=1)
        date_to = date_time_obj.date()

        title_data = str(event['employee_id'][1])+" on "+str(event['holiday_status_id'][1])+" : "+str(event['number_of_days'])+" days"
        color_data = ""
        classname1 = ""
        if event['state'] == "validate":
            classname1 = "bg-success"
        elif event['state'] == "validate1":
            classname1 = "bg-info"
        elif event['state'] == "refuse":
            classname1 = "bg-danger"
        elif event['state'] == "confirm":
            classname1 = "bg-warning"
        elif event['state'] == "draft":
            classname1 = "bg-dark"
        out.append({



            'title':title_data,
            'id':event['id'],
            'start': event['date_from'],
            'end': date_to,
            'color':color_data,
            'className':classname1
        })
    return JsonResponse(out, safe=False)


def employee_events(request):
    type1 = request.GET.get("type")
    leave_type = request.GET.get("leave_type")
    li = type1.split(',')
    list2 = list(map(int, li))
    user_auth_id = request.user.id
    odoo_id = 0
    leave_type_list = leave_type.split(",")
    list3 = list(map(int, leave_type_list))
    try:

        odoo_data = User_Management.objects.get(auth_user=user_auth_id)
        odoo_id = odoo_data.odoo_id

    except:
        pass
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    leave_history_response = ""
    try:
        leave_history_response_url = api_domain + "api/get_leave_history_calender"
        leave_history_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {

            "employee_ids" : list2,
            "all": "True",
            "start_date" : "2022-07-01",
            "end_date" : "2022-07-31",
            'type_ids':list3
            }
        })
        leave_history_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers,
                                                   data=leave_history_payload).json()

        leave_history_response12 = leave_history_response1['result']
        leave_history_response = leave_history_response12['result']



    except:
        pass
    out = []
    for event in leave_history_response:
        from datetime import datetime
        df = datetime.fromisoformat(event['date_to'])
        from datetime import timedelta
        date_time_obj = df + timedelta(days=1)
        date_to = date_time_obj.date()
        title_data = str(event['employee_id'][1]) + " on " + str(event['holiday_status_id'][1]) + " : " + str(event['number_of_days']) + " days"
        color_data = ""
        classname1 = ""
        if event['state'] == "validate":
            classname1 = "bg-success"
        elif event['state'] == "validate1":
            classname1 = "bg-info"
        elif event['state'] == "refuse":
            classname1 = "bg-danger"
        elif event['state'] == "confirm":
            classname1 = "bg-warning"
        elif event['state'] == "draft":
            classname1 = "bg-dark"
        out.append({

            'title': title_data,
            'id': event['id'],
            'start': event['date_from'],
            'end': date_to,
            'color': color_data,
            'className': classname1
        })
    return JsonResponse(out, safe=False)




def cal_depended(request):
    dt=request.GET.get('date_emp')
    from datetime import datetime
    dd=datetime.fromisoformat(dt[:-1])
    date = dd.date()
    date_month=str(date.year)+'-'+str(date.month)
    user_auth_id = request.user.id
    odoo_id = 0
    try:

        odoo_data = User_Management.objects.get(auth_user=user_auth_id)
        odoo_id = odoo_data.odoo_id

    except:
        pass
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token

    child_response = ""
    try:
        child_response_url = api_domain + "api/get_childs"
        child_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {

                "employee_id" : odoo_id,
                "date" : date_month,
                "leave_gantt" : "True",
                "leave_type_include" : "True"
            }
        })
        child_header = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        child_response1 = requests.request("GET", child_response_url, headers=child_header, data=child_payload).json()
        child_response12 = child_response1['result']
        child_response = child_response12['result']
    except:
        pass
    leave_type = []
   
    for i in child_response:
        for j in i['leave_types']:
            leave_type.append({

                'id': j[0],
                'name': j[1]
            })
    seen = set()
    new_l = []
    for d in leave_type:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    context = {
        'child_response': child_response,
        'leave_list_data':new_l
    }

    return render(request, 'super_admin/cal_depended.html', context)





def username_exists_condition(request):
    username = request.GET.get("username",False)
    print("username:::::",str(username))
    data = []
    if User.objects.filter(username=username).exists():
        data = {"message":"True"}
        return JsonResponse(data,safe=False)
    else:
        data = {"message":"False"}
        return JsonResponse(data,safe=False)


def test_current_address(request):
    print("test addresss")
    import geocoder
    g = geocoder.ip('me')
    print("addresss",str(g.address))
    print(g.latlng)
    print("ip:::",str(g.ip))
    print("hostname:::",str(g.hostname))
    print("city::::",str(g.city))
   
    print("country:::",str(g.country))
  
    print("org:::",str(g.org))
    print("postal::",str(g.postal))







def user_login_log(request):
    user_login_log_history_data = user_login_log_history.objects.all().order_by('-id')
    return render(request,'super_admin/user_login_log.html',{'user_login_log_history_data':user_login_log_history_data})


def user_login_log_date_filter_action(request):
    if request.method == "POST":
        filter_dt = request.POST.get("filter_dt",False)
        user_login_log_history_data = user_login_log_history.objects.filter(dt=filter_dt).order_by('-id')
        return render(request,'super_admin/user_login_log.html',{'user_login_log_history_data':user_login_log_history_data})
    



def test_gantt_chart(request):
    import calendar
    import datetime
    now = datetime.datetime.now()

    days = calendar.monthrange(now.year, now.month)[1]
  
    month_num = str(now.month)
    datetime_object = datetime.datetime.strptime(month_num, "%m")

    month_name = datetime_object.strftime("%b")
  

    full_month_name = datetime_object.strftime("%B")


    employee_data = User_Management.objects.get(auth_user=request.user)

    import datetime, calendar
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]

    year = now.year
    month = now.month


    get_chile_response = ""
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    send_data = str(year)+"-"+str(month)
    try:
        get_chile_response_response_url = api_domain+"api/get_childs"
        get_chile_response_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id": int(employee_data.odoo_id),
               
                'leave_gantt':"True",
                "date" : send_data
            }
        })
        get_chile_response_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        get_chile_response1 = requests.request("GET", get_chile_response_response_url, headers=get_chile_response_headers, data=get_chile_response_payload).json()
        
        
        get_chile_response112  = get_chile_response1['result']
        get_chile_response = get_chile_response112['result']
        
       
        

    except:
        pass




    



    
    print("month_name::::",str(month_name))
    context = {
        'full_month_name':month_name,
        'days':days,
        'employee_data_name':employee_data.employee_name,
        'ays':ays,
        'year':year,
        'month':month,
        'get_chile_response':get_chile_response,
        'send_data':send_data
    }
    return render(request,'super_admin/test_gantt_chart.html',context)




def role_exists_check(request):

    role = request.GET.get("role",False)

    print("role:::::",role)

    if Role_details.objects.filter(role_name=role).exists():

        data = "exist"

        return JsonResponse(data,safe=False)

    else:

        data = "success"

        return JsonResponse(data,safe=False)



def profile(request):
    data = ""
    try:
        data = User_Management.objects.get(auth_user=request.user)
    except:
        pass
    context = {
        'data':data
    }
    return render(request,'super_admin/profile.html',context)



def pattern_lock(request):
    return render(request,'super_admin/pattern_lock.html')



def set_lock_pattern(request):
    data = False
    try:
        data = pattern_lock_table.objects.get(auth_user_id= request.user)
        print("kkkkkkkkkkkkkk666666666666666666666kkkk")
        data = True
    except:
        data = False
        pass
    return render(request,'super_admin/set_lock_pattern.html',{'data':data})



def pattern_lock_submit_action(request):

    if request.method == "POST":
        lock = request.POST.get("lock",False)
        print("lock:::",str(lock))

        data_save = pattern_lock_table(
            auth_user_id= request.user,
            pattern_number=lock,
            status = "True"
        )
        data_save.save()
        return redirect("admin_dashboard")



def pattern_login_action(request):

    if request.method == "POST":
        lock = request.POST.get("lock")

        try:
            data = pattern_lock_table.objects.get( auth_user_id= request.user,pattern_number=lock)
            data_update = pattern_lock_table.objects.filter( auth_user_id= request.user,pattern_number=lock).update(status="login")
            return redirect("admin_dashboard")
        except:
            return redirect("pattern_lock")
            pass



def logoutconfirmation(request):
    try:
        data_update = pattern_lock_table.objects.filter( auth_user_id= request.user).update(status="True")
    except:
        pass
    return redirect("logout")



def remove_pattern_lock(request):
    data_delete = pattern_lock_table.objects.filter( auth_user_id= request.user)
    data_delete.delete()
    return redirect("admin_dashboard")


def change_password(request):

    return render(request,'super_admin/change_password.html')



def update_password(request):

    if request.method == "POST":



        username = request.user

        print("userrrrrrrrrrr",username)

        oldpass = request.POST.get('oldpass')

        print("oldpassword::::::;;",oldpass)

        newpass = request.POST.get("newpass")

        print("newpassword:::::::::",newpass)

        confirmpass = request.POST.get("confirmpass")

        print("confirmpassword:::::::;;",confirmpass)



        if newpass == confirmpass :



            user = authenticate(username=username,password=oldpass)

            if user is not None:

                user.set_password(newpass)

                user.save()

                print("---updated------")

            else:



                print('user is not exist')

                messages.warning(request,str("error"))

                return redirect('change_password')



            if(User_Management.objects.filter(username = username , password = oldpass).exists()):

                print("heyyyyyyyyy")

                User_Management.objects.filter(username = username).update(password=newpass)
                

                return redirect('index')

            else:

                print('user is not exist')   

        else:

            messages.warning(request,str("notequal"))

            return redirect('change_password')       

    return redirect('index')




def user_leave_apply_to_draft_action(request):

    if request.method == "POST":
        try:
            employee_attached_file = request.FILES['employee_attached_file']
            print("employee_attached_file:::",str(employee_attached_file))
        except:
            employee_attached_file = None

        print("-------------data-----------------------???????????????")
        employee_name1 = request.POST.get("employee_name1",False)
        leave_type_nm = request.POST.get("leave_type_nm",False)
        employee_name = request.POST.get("employee_name",False)
        print("employee_name::::",str(employee_name))
        employee_email = request.POST.get("employee_email",False)
        employee_number = request.POST.get("employee_number",False)
        employee_leave_type = request.POST.get("employee_leave_type",False)
        employee_leave_from_date = request.POST.get("employee_leave_from_date",False)
        employee_leave_to_date = request.POST.get("employee_leave_to_date",False)
        employee_available_leave = request.POST.get("employee_available_leave",False)
        employee_leave_reason = request.POST.get("employee_leave_reason",False)
        employee_total_days = request.POST.get("employee_total_days",False)
        employee_leave_replacer = request.POST.get("employee_leave_replacer",False)
        employee_alternative_contcat_no = request.POST.get("employee_alternative_contcat_no",False)
        request_unit_half= request.POST.get("request_unit_half",False)
        absence_status = request.POST.get("absence_status",False)
        absence_category = request.POST.get("absence_category",False)
        employee_replacer_text = request.POST.get("employee_replacer_text",False)
        if request_unit_half == "Half day":
            employee_leave_to_date = employee_leave_from_date
            pass

        request_date_from_period = request.POST.get("request_date_from_period",False)
        if employee_leave_type == 'no':
            employee_leave_type = None
        user_data = User_Management.objects.get(auth_user=request.user)
        if employee_leave_to_date == '':
            employee_leave_to_date = None
        if employee_total_days == '':
            employee_total_days = None
        if employee_leave_from_date == '':
            employee_leave_from_date = None
        data_save_draft = User_leave_draf_history(
            auth_user_id = request.user,
            user_id_id= user_data.id,
            leave_type = leave_type_nm,
            from_date = employee_leave_from_date,
            to_date = employee_leave_to_date,
            total_days = employee_total_days,
            reason = employee_leave_reason,
            alternative_contact_number = employee_alternative_contcat_no,
            employee_leave_replacer = employee_leave_replacer,
            employee_id = employee_name,
            request_unit_half = request_unit_half,
            request_date_form_period = request_date_from_period,
            absence_status = absence_status,
            absence_category = absence_category,
            leave_type_id = employee_leave_type,
            employee_name = employee_name1,
            status = "pending",
            employee_reg_number = employee_number,
            employee_replacer_name=employee_replacer_text,
            attached_file= employee_attached_file
            


        )
        data_save_draft.save()




        data = []
        data = {
            'message':'success'
        }
        return JsonResponse(data,safe=False)
        pass





def leave_draft_modal_action(request):
    id = request.GET.get("id",False)
    print("id:::::::::::",str(id))
    return render(request,'super_admin/leave_draft_modal.html')


@csrf_exempt
def upload_img1(request):
    if request.method == "POST":
        filename = request.FILES['files']
        print("files:::",str(filename))
        data_save = test_file_upload(
            file_data = filename
        )
        data_save.save()


def demo(request):
    print("gggg")
    if request.method == "POST":
        img = request.FILES['img']
        print("img:::::::::",str(img))
    data = test_file_upload.objects.get(id=14)
    from PIL import Image 
    import PIL 

    url = 'http://127.0.0.1:8000/upload_img1'
    image_url = data.file_data.url
    print("image_url:::::",str(image_url))
  
    # files = {'video_path': open(f2, 'rb')}
    files={'files': open('.'+image_url,'rb')}
    values = {
                'file_name':str("DEMOOOO")
    }
    r = requests.post(url, files=files,data=values)

    # data_save = test_file_upload(
    #     file_data = files
    # )
    # data_save.save()

    df = test_file_upload.objects.all().order_by('-id')
    df1 = df[5:6]
    print("values::::")
    print(df1.values_list())


  

    
    
    context = {
        'data':data
    }
   

    return render(request,'super_admin/demo.html',context)




def get_employee_validate_entitle_balance(request):
    employee_id = request.GET.get("employee_id",False)
    print("employee_id:::",str(employee_id))
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    entitlement_balances_url = api_domain+"api/get_leave_entitlement"
    entitlement_balances_payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id" : int(employee_id)
               
        }
    })
    entitlement_balances_header = {
        'api_key': odoo_token_data.token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    entitlement_balances_response1 = requests.request("GET", entitlement_balances_url, headers=entitlement_balances_header, data=entitlement_balances_payload).json()
    entitlement_balances_response12 = entitlement_balances_response1['result']
    entitlement_balances_response = entitlement_balances_response12['result']
    return render(request,'super_admin/get_selected_employee_entitlement_balance.html',{'entitlement_balances_response':entitlement_balances_response})



def user_enable_email_otp(request):
    status = False
    try:
        data = Login_otp.objects.get(auth_user_id=request.user)
        status = True
    except:
        pass

    return render(request,'super_admin/user_enable_email_otp.html',{'status':status})



def email_otp_authentication_enable_action(request):
    if request.method == "POST":
        email = request.POST.get("email",False)
        print("email::::",str(email))
        try:
            data = Login_otp.objects.get(auth_user_id=request.user)
        except Login_otp.DoesNotExist:
            data_save = Login_otp(
                otp_type = "email_otp",
                email = email,
                status = "True",
                auth_user_id = request.user
            )
            data_save.save()
        return redirect("admin_dashboard")


def email_otp_disable_action(request):
    data_delete =  Login_otp.objects.get(auth_user_id=request.user)
    data_delete.delete()
    return redirect("admin_dashboard")


def email_otp_action(request):
    if request.method == "POST":
        username = request.POST.get("username",False)
        password = request.POST.get("password",False)
        print("username::::",str(username))
        print("password:::::",str(password))
        user = authenticate(username=username, password=password)
        import random
        fixed_digits = 5
        data = random.randrange(11111, 99999, fixed_digits)
        email_data = Login_otp.objects.get(auth_user_id_id=user.id)
        import smtplib
        from email.message import EmailMessage
        msg = EmailMessage()
        msg.set_content('your otp is '+str(data))
        msg['Subject'] = 'TSS APP LOGIN OTP'
        msg['From'] = "amrithakumar34@gmail.com"
        msg['To'] = str(email_data.email)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("amrithakumar34@gmail.com", "uehxynftlsmrvuly")
        server.send_message(msg)
        server.quit()
        update_data = Login_otp.objects.filter(auth_user_id_id=user.id).update(otp=data)
        return render(request,'super_admin/email_otp.html',{'username':username,'password':password})



def email_otp_verification_action(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    otp = request.GET.get("otp")
    print("user_name::::",str(username))
    print("password:::",str(password))
    print("otp:::::",str(otp))
    user = authenticate(username=username, password=password)
    data = []
    try:
        data1 =  Login_otp.objects.get(auth_user_id_id=user.id,otp=otp)
        data = {
            'message':'success'
        }
        return JsonResponse(data,safe=False)
    except Login_otp.DoesNotExist:
        data = {
            'message':'error'
        }
        return JsonResponse(data,safe=False)


def notification_card_view(request):
    count = request.GET.get("count",False)
    print("count::::::::::::",str(count))
    notifictaion = odoo_notification.objects.filter(auth_user_id=request.user,category="notification").order_by('-id')
    
    count1 = int(count) + 10
    
    notifictaion = notifictaion[int(count):int(count1)]
    print("------------->>>>>>>>>>>>>")
    print(notifictaion.values_list())
    return render(request,'super_admin/notification_card_view.html',{'notifictaion':notifictaion})







def pettycash_action(request):

    if request.method == "POST":
        amount_requested = request.POST.get("amount_requested",False)
        job_no = request.POST.get("job_no",False)
        purpose = request.POST.get("purpose",False)
        iban_no = request.POST.get("iban_no",False)
        payment_type = request.POST.get("payment_type",False)
        supplier_data = request.POST.get("supplier_data",False)
        employee_attached_file = None
        try:
            employee_attached_file = request.FILES['employee_attached_file']
        except:
            pass
        user_data = User_Management.objects.get(auth_user=request.user)
        print("user_data.id::::;;",user_data.id)
        odoo_id = user_data.odoo_id
        pettycash_url = api_domain+"api/post_pettycash"
        payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "odoo_id": odoo_id,
                "amount_requested": amount_requested,
                "job_no": job_no,
                "purpose": purpose,
                "iban_no": iban_no,
            }
        })
        odoo_token_data = odoo_api_request_token.objects.get(status="True")

        headers = {
        'api_key': odoo_token_data.token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        print("responsee///////")
        response1 = requests.request("POST", pettycash_url, headers=headers, data=payload)
        response2 = response1.json()['result']
        print("respose2:::::;;",response2)
        l1 = response2['result']

        return JsonResponse(data,safe=False)
        return redirect("petty_cash_management")




@csrf_exempt
def test_post_api(request):
    print("-------------methodddddd")
    if request.method == "POST":
        print("----------------------***************")
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode) 	
        print(body)
        
        uname = request.POST.get("username",False)
        password = request.POST.get("password",False)
        print("uname::::::",str(uname))
        print("password::::",str(password))
        return JsonResponse({"message":"success"})




class odoo_leave_reassign_api(APIView):

    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        data = request.data
        leave_id = data['leave_id']
        state = data['state']
        responsible_for_approval_user_id = data['responsible_for_approval_user_id']
        activity_done_by = data['activity_done_by']
        activity_user = User_Management.objects.get(odoo_id=activity_done_by)
        approval_user = User_Management.objects.get(odoo_id=responsible_for_approval_user_id)
        data_update_approve_status = odoo_notification.objects.filter(mapping_id=leave_id,auth_user_id=activity_user.auth_user,notification_type="leave_approve_request",status="Pending").update(status="reassign",read_status=1)
        data_update_requested_user_status = odoo_notification.objects.filter(mapping_id=leave_id,notification_type="leave_type").update(status=state,read_status=0)
        next_approve_user_data = ""
        try:
            next_approve_user_data = User_Management.objects.get(odoo_id=int(responsible_for_approval_user_id)) 
        except:
            pass
        try:
            leave_data = odoo_notification.objects.get(mapping_id=leave_id,notification_type="leave_type")
        except:
            leave_data = odoo_notification.objects.get(mapping_id=leave_id,auth_user_id=activity_user.auth_user,notification_type="leave_approve_request")
            pass
        try:
            next_approval_notification = odoo_notification(
                notification_type="leave_approve_request",
                message="leave request",
                mapping_id = leave_id,
                requested_from_dt = leave_data.requested_from_dt,
                requested_to_dt = leave_data.requested_to_dt,
                read_status = 0,
                status = "Pending",
                auth_user_id_id = next_approve_user_data.auth_user.id,
                leave_type_name = leave_data.leave_type_name,
                leave_apply_user_name = leave_data.leave_apply_user_name,
                description = "null",
                current_leave_status = state,
                category = "activities"
            )
            next_approval_notification.save()
        except:
            pass 
        try:
            leave_status_update = Leave_Status_details.objects.filter(auth_user=activity_user.auth_user).update(status="Reassigning",note=next_approve_user_data.employee_name)
        except:
            pass
        from datetime import date
        today = date.today()
        try:
            add_leave_status = Leave_Status_details.objects.create(
                leave_mapping_id = int(leave_id),
                user_name = next_approve_user_data.employee_name,
                auth_user = next_approve_user_data.auth_user,
                dt = today,
                status = "Pending"
            )
        except:
            pass

        content = {
           "message":"success"
        }
        return Response(content)
    



def user_switch_company_and_branch(request):
    employee_company_instance = User_company_details.objects.filter(auth_user_id=request.user)
    context = {
        'employee_company_instance':employee_company_instance
    }
    return render(request,'super_admin/user_switch_company_and_branch.html',context)



def update_active_company_action(request):
    if request.method == "POST":
        company = request.POST.get("company",False)
        branch = request.POST.get("branch",False)
        print("company::::::",str(company))
        print("branch:::::",str(branch))
       
        data_check = User_company_based_branch_details.objects.get(id=branch)
        company_id = data_check.company_id.id
        print("company_id::::",str(company_id))
        if int(company) == int(company_id):
            update_company1 = User_company_details.objects.filter(auth_user_id=request.user.id).update(status=False)
            update_branch = User_company_based_branch_details.objects.filter(company_id__auth_user_id=request.user.id).update(status=False)

            update_company = User_company_details.objects.filter(id=company).update(status=True)
            update_branch1 = User_company_based_branch_details.objects.filter(id=branch).update(status=True)


            company_data = User_company_details.objects.get(id=company)
            branch_data = User_company_based_branch_details.objects.get(id=branch)
            updated_user = User_Management.objects.filter(auth_user=request.user).update(employee_company_id=company_data.company_id,company_name=company_data.company_name,employee_branch=branch_data.branch_name,employee_branch_id=branch_data.branch_id,odoo_id=company_data.odoo_id)
            return redirect(request.META['HTTP_REFERER'])
        else:
             messages.warning(request,str("The selected company and branch are incompatible in the equal to operator"))
             return redirect(request.META['HTTP_REFERER'])





def test_petty_cash(request):
    if request.method == "POST":
        attachment_image_value = request.POST.get("attachment_image_value")
        print("count:::",str(attachment_image_value))
        for i in range(0,int(attachment_image_value)+1):

            data_value = request.POST.getlist("values_list"+str(i)+"[]")
            print("------------start_path-------------------  ")
            print(data_value)         
            print("----dddd")
            
            print("----------endpath---------------")
        
        pass
    else:
        return render(request,'super_admin/test_petty_cash.html')

    


from django.contrib.auth.forms import UserCreationForm

from .form import createUserForm
from django.contrib import messages
def user_creation_form(request):

    if request.method == "POST":
        print("-------post")
        form = createUserForm(request.POST)
        print("-------form post")
        if form.is_valid():
            print("-----valid form")
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+user)
            return
        else:
            print("not valid form")
        context = {
            'form':form
        }
        return render(request,'super_admin/user_creation_form.html',context)    
        pass
    form = createUserForm
    context = {
        'form':form
    }
    return render(request,'super_admin/user_creation_form.html',context)




class user_company_update_api(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        data = request.data
        existing_employee_id = data["existing_employee_id"]
        employee_id = data["employee_id"]
        company_id = data["company_id"]
        company_name = data["company_name"]
        branch_id = data["branches"][0]['id']
        branch_name = data["branches"][0]['name']
        deleted = data["deleted"]

        try:
            existing_user = User_company_details.objects.get(odoo_id=int(existing_employee_id))
            existing_auth_user = existing_user.auth_user_id

            if (User_company_details.objects.filter(auth_user_id=existing_auth_user,company_id=company_id).exists()):
                company_data_existance = User_company_details.objects.filter(auth_user_id=existing_auth_user,company_id=company_id)
                company_data = company_data_existance[0]
                if(User_company_based_branch_details.objects.filter(company_id=company_data,branch_id=branch_id).exists()):
                    pass
                else:
                    branch_data = User_company_based_branch_details(company_id=company_data, branch_name=branch_name,
                                                                    branch_id=branch_id)
                    branch_data.save()
            else:

                company_data = User_company_details.objects.create(auth_user_id=existing_auth_user, user_id_id=existing_user.user_id.id,
                                                                   company_name=company_name, company_id=company_id,
                                                                   odoo_id=employee_id,status=deleted)
                
                branch_data = User_company_based_branch_details(company_id_id=company_data.id, branch_name=branch_name,
                                                                               branch_id=branch_id)
                branch_data.save()
        except:
            if(deleted == True):
                data_delete = User_company_details.objects.filter(odoo_id=employee_id,company_id=company_id)
                data_delete_object = data_delete[0]
                data_delete_object.delete()
            else:
                pass
        data_json = {
            'message': "success"
        }
        return JsonResponse(data_json, safe=False)