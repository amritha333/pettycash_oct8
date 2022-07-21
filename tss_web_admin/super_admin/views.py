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
        print("---not exists---")





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





api_domain = "http://10.10.10.107:8069/"



@login_required(login_url='/index')
def admin_dashboard(request):
    user = request.user
    
    user_dat = User.objects.get(id=request.user.id)
    st = user_dat.is_superuser
    print("status:::::",str(st))

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
    print("user_login_id::::",str(user_login_id))
    return render(request,'super_admin/user_home.html')
import json

def login_action(request):

    if request.method == "POST":
        from datetime import date
        uname = request.POST.get("uname",False)
        passwrd = request.POST.get("passwrd",False)
        print("uname:::",str(uname))
        print("passwrd:::",str(passwrd))
        user = authenticate(username=uname, password=passwrd)
        remember = request.POST.get("remember",False)
        print("rem::::",str(remember))
        
        
        if user is not None:
            if remember == "yes":
                request.session['user_email'] = uname
            else:
                request.session['user_email'] = ""

            st = user.is_superuser

            token_url = api_domain+"api/get_api_key"
            payload = json.dumps({
                "jsonrpc": "2.0",
                "params": {
                "login": "admin",
                "password": "admin",
                "db": "tss-latest"
                }
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': 'session_id=9d67dcc82ed899ef3c1b3bbe0b6377464c46a52d'
            }

            response = requests.request("GET", token_url, headers=headers, data=payload)
            print("odooooooo")

            json_response = response.json()['result']

            print("result::::::")
            print(json_response['result'])

            try:
                alredy_exists_odoo_token = odoo_api_request_token.objects.get(status="True")
                if alredy_exists_odoo_token is not None:
                    update_token =  odoo_api_request_token.objects.filter(status="True").update(
                        token = json_response['result']
                    
                    )

            except odoo_api_request_token.DoesNotExist:
                save_token = odoo_api_request_token(
                    token = json_response['result'],
                    status = "True" 
                )
                save_token.save()


            
            print("user_type::::",str(st))
            print("login sucess")

            login(request, user)

            if st == True:


                return redirect("admin_dashboard")
            elif st == False:
                today = date.today()

                
                try:
                    login_effective = User_Management.objects.filter(auth_user=user,effective_to_dt__gte=today,effective_from_dt__lte=today) | User_Management.objects.filter(auth_user=user,effective_from_dt__lte=today,effective_to_dt=None)
                    if login_effective:
                        return redirect("admin_dashboard")
                    else:
                        date_data = User_Management.objects.get(auth_user=user)
                        login_date = date_data.effective_from_dt
                        context={
                            'message':"login_date_error",
                            'login_date':login_date
                        }
                        return render(request,'super_admin/index.html',context)

                except User_Management.DoesNotExist:
                    date_data = User_Management.objects.get(auth_user=user)
                    login_date = date_data.effective_from_dt
                    context={
                        'message':"login_date_error",
                        'login_date':login_date
                    }
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
                print("login error")
                context['message'] = "error"
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
    print("username:::",str(username))

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

        print("id::::::::::",str(instance.id))
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
        print("id::::::",str(id))
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

    print("userlogin_id::::",str(user_login_id))




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
        print("onward_journey:::::",str(onward_journey))
        print("return_journey::::::",str(return_journey))
   
        

        



        











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
        

@test_w1('Employee')
@login_required(login_url='/index')
def employee_master(request):



    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token
    print("odoo_token:::::",str(odoo_token))


    url = api_domain+"api/get_employees"

    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {}
    })
    headers = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    response1 = response.json()['result']


   
    
    

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
    


    address_response = api_domain+"api/get_employee_addreess"
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
    address_response = requests.request("GET", address_response, headers=address_headers, data=address_payload)
   
    address_res = address_response.json()['result']['result']
    


    
    # response =False
    # try:
    #     response = requests.get(api_domain+"api/get_employee?empl_id="+employee_id).json()[0]
    # except:
    #     pass
    


    # dept = False
    # try:
    #     dept = response['department_id'][1]
    # except:
    #     pass
    # print("depatment:::",str(dept))


    # print("r1:::::::",str(response))
    # address_id = response['address_home_id'][0]
    # print("address_id:::::",str(address_id))

    # address_response = requests.get(api_domain+"api/get_employee_addreess?partner_id="+str(address_id)).json()[0]
    # print("address_response::::")
    # print(address_response)


    # state = False
    # try:
    #     state = address_response['state_id'][1]
    # except:
    #     pass
    # country_id = False
    # try:
    #     country_id = address_response['country_id'][1]
    # except:
    #     pass

    
    context = {
        'response':data_response,
        'dept':"test",
        'address_response':address_res[0],
        'state':"test",
        'country_id':"test"
    }
    return render(request,'super_admin/employee_more_details.html',context)

from datetime import date


@test_w1('User')
@login_required(login_url='/index')
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
        


    




    

    data_base_exists_employee_id = User_Management.objects.all()

    data_exists_employee = list(data_base_exists_employee_id.values_list("odoo_id",flat=True))

    
    

    params_data  = ",".join(data_exists_employee)
    
    select_employee_api = ""
    
    try:
        odoo_token_data = odoo_api_request_token.objects.get(status="True")
        odoo_token = odoo_token_data.token
        employee_data_url =api_domain+"api/get_employees"
        
        payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
            "employee_ids": data_exists_employee
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

    # print("select_employee:::::",str(select_employee_api))
    
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
    print("employee_id:::::::::",str(employee_id))
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

    response1  = requests.request("GET", employee_data_url, headers=headers, data=payload).json()
    response12 =response1['result']
    response = response12['result'][0]
   
    print("response1222222:::::",str(response))
    name = ""
    employee_dpt = ""
    employee_branch = ""
    emp_registration_id = ""
    name = response['name']
    company_name = response['company_id']
    print("company_name:::",str(company_name[1]))
    try:
        employee_dpt  = response['department_id'][1]
    except:
        employee_dpt = False
    try:
        employee_branch = response['branch_id'][1]
    except:
        employee_branch = False
    emp_registration_id = response['registration_number']
    
   
    

        
        

        
        
        
        


    data = {
        "employee_branch" :employee_branch,
        "employee_dpt":employee_dpt,
        "employee_name":name,
        "emp_registration_id":emp_registration_id,
        'company_name':str(company_name[1])
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
        
        username = request.POST.get("username",False)
        password_option = request.POST.get("password_option",False)
        if User.objects.filter(username=username).exists():
            messages.warning(request,str("Unexpected error:An account with the given username alredy exists"))
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
        print("effective_to_dt::::",str(effective_to_dt))
        if effective_to_dt == "":
            effective_to_dt = None
        employee_branch = request.POST.get("employee_branch",False)
        
         
        employee_id = request.POST.get("employee_id",False)
        print("employee_id::::::::::",str(employee_id))

        if employee_id == '0':
            
            pass
        else:
            print("branch::",str(employee_branch))
            if employee_branch == "false":
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
        print("role_lenth::::",str(role_length))

        emp_registration_id = request.POST.get("emp_registration_id",False)

        print("password_expiration_option:::",str(password_expiration_status))

        if password_expiration_status == "days":
            passsword_used_days = request.POST.get("passsword_used_days",False)
            print("passsword_used_days::::::",str(passsword_used_days))

            from datetime import timedelta, date
            EndDate = date.today() + timedelta(days=int(passsword_used_days))
            print("password_end_date:::::",str(EndDate))
            try:
                user_alredy_exists_condition = User_Management.objects.get(employee_id=employee_id)
                if user_alredy_exists_condition is not None:
                    print("----user alredy exists----")
                
                url = redirect("user_management")
                print("url", url.url)
        
                return HttpResponseRedirect(url.url + '?message=' + "already_exists")
            except User_Management.DoesNotExist:

                if employee_id == 0:
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    data1 = Token.objects.create(user=user)
                    print(data1.key)
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
                        company_name = company_name



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
                   
                        print("----enddddddddd")

                


                else:
                    print("------ssssssss----")
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    data1 = Token.objects.create(user=user)
                    print(data1.key)
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
                        company_name = company_name


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
                   
                        print("----enddddddddd")
                
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
                    print("----user alredy exists----")
                
                url = redirect("user_management")
                print("url", url.url)
        
                return HttpResponseRedirect(url.url + '?message=' + "already_exists")

            except User_Management.DoesNotExist:
                print("------ssssssss----")
                if employee_id == 0:
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    data1 = Token.objects.create(user=user)
                    print(data1.key)
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
                        company_name = company_name


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
                   
                        print("----enddddddddd")
                else:
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    data1 = Token.objects.create(user=user)
                    print(data1.key)
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
                        company_name = company_name


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
                   
                        print("----enddddddddd")
                messages.success(request,str("password:"+str(password)))
                return redirect("user_management")







     

        



def view_user_more_details(request):

    id = request.GET.get("id",False)
    print("id:::::::",str(id))
    data = User_Management.objects.get(id=id)

    user_role_details = user_role_mapping.objects.filter(user_id_id=id)

    context = {
        'data':data,
        'user_role_details':user_role_details
    }
    return render(request,'super_admin/view_user_more_details.html',context)




def edit_user_more_details(request):
    id = request.GET.get("id",False)
    print("id::::",str(id))

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
    print("role_id:::::::",str(role_id))
    print("value:::::",str(value))
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


        print("edit_password_expiration:::::::",str(edit_password_expiration))
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
                print("password_end_date:::::",str(EndDate))
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
                employee_name = employee_name

                
            )

            user_details = User_Management.objects.get(id=user_updated_id)

            u = User.objects.get(id=user_details.auth_user.id)
            u.set_password(password)
            u.save()
            update_auth_username = User.objects.filter(id=user_details.auth_user.id).update(username=username)
            pass




        



        role_data = user_role_mapping.objects.filter(user_id_id=user_updated_id)
        print("role_data:::::::")
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
                print("----updated log---------------")

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
                print("-------------no updated-----------------")
            print("--------------------end-----------------------------------------")

        



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



def leave_management(request):


    user_auth_id = request.user.id
    print("user_auth_id::::",str(user_auth_id))
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

    print("odoo_id::::::",str(odoo_id))
   
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
    odoo_token = odoo_token_data.token

    leave_history_response = ""
    try:
        leave_history_response_url = api_domain+"api/get_leave_history"
        leave_history_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id": int(odoo_id)
            }
        })
        leave_history_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers, data=leave_history_payload).json()
        print("rs122223::::")
        print("response1::::::::")
        print(leave_history_response1)
        
        leave_history_response12  = leave_history_response1['result']
        leave_history_response = leave_history_response12['result']
        print("r1::")
        print(leave_history_response)
        

    except:
        pass

    leave_type_response = ""
    try:
        leave_type_response_url = api_domain+"api/get_leave_types"
        leave_type_payload = json.dumps({
             "jsonrpc": "2.0", 
             "params": {
            }
        })
        leave_type_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'

        }
        leave_type_response1 = requests.request("GET", leave_type_response_url, headers=leave_type_headers, data=leave_type_payload).json()
        leave_type_response12 = leave_type_response1['result']
        leave_type_response = leave_type_response12['result']
    except:
        pass
    
    replacer_response = ""
    try:
        replacer_api_url = api_domain+"api/get_employees"
        replacer_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
               
            }
        })
        replacer_header = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        replacer_response1 = requests.request("GET", replacer_api_url, headers=replacer_header, data=replacer_payload).json()
        replacer_response12 = replacer_response1['result']
        replacer_response = replacer_response12['result']
    except:
        pass
    # replacer_response = requests.get(api_domain+"api/get_all_employees").json()




    
    child_response = ""
    try:
        child_response_url = api_domain+"api/get_childs"
        child_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id" : int(odoo_id)
               
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




    entitlement_balances_url = api_domain+"api/get_leave_entitlement"
    entitlement_balances_payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id" : int(odoo_id)
               
        }
    })
    entitlement_balances_header = {
        'api_key': odoo_token,
        'Content-Type': 'application/json',
        'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
    }
    entitlement_balances_response1 = requests.request("GET", entitlement_balances_url, headers=entitlement_balances_header, data=entitlement_balances_payload).json()
    entitlement_balances_response12 = entitlement_balances_response1['result']
    entitlement_balances_response = entitlement_balances_response12['result']
    
    


    context = {
        'leave_type_response':leave_type_response,
        'leave_history_response':leave_history_response,
        'emp_name':emp_name,
        'emp_email':emp_email,
        'emp_id':emp_id,
        'replacer_response':replacer_response,
        'child_response':child_response,
        'entitlement_balances_response':entitlement_balances_response,
        'child_count':len(child_response)
        
    }

    return render(request,'super_admin/leave_management.html',context)




def get_total_available_leave_count(request):

    leave_type = request.GET.get("leave_type",False)
    print("leave_type:::::",str(leave_type))
    selected_employee_id = request.GET.get("selected_employee_id",False)
    odoo_login_id = 0
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
        
        print(leave_available_response12)
    
    except:
        pass



    
    

    leave_type_name = ""
    total_available_leave = 0
    annual_status = False

    print("r1:::")
    print(leave_available_response)

    
    print("l1:::")
    



    

    try:
        
        leave_type_name = str(leave_available_response['type_name'])
        total_available_leave = str(leave_available_response['remaining_leaves'])
        annual_status = leave_available_response[0]['is_annual_vacation']
        
    except:
        pass

    

    

    print("odoo_login_id:::::::",str(odoo_login_id))

    data= {
        'respose_status':respose_status,
        'total_available_leave' :total_available_leave ,
        'leave_type_name':leave_type_name,
        'annual_status':annual_status,
        'half_day_status':half_day_status,
        'requires_allocation':requires_allocation
    }
        
    return JsonResponse(data,safe=False)



def petty_cash_management(request):
    return render(request,'super_admin/petty_cash_management.html')


def advance_salary_management(request):
    return render(request,'super_admin/advance_salary_management.html')


def role_edit_modal_function(request):
    id = request.GET.get("id",False)
    print("id::::::::::",str(id))
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
    print("id::::::::::",str(id))
    data = User_Management.objects.get(id=id)

    user_role_details = user_role_mapping.objects.filter(user_id_id=id)


    role_data = Role_details.objects.all()




    context = {
        'data':data,
        'user_role_details':user_role_details,
        'role_data':role_data
    }

    return render(request,'super_admin/user_edit_modal_function.html',context)



def user_role_log_modal(request):
    id = request.GET.get("id",False)
    print("id:",str(id))

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
        print("name::::",str(name))
        messages.success(request, 'Passwords are not same.!')
        return redirect('index')
    
    return render(request,'super_admin/index.html')




def user_leave_apply_action(request):
    if request.method == "POST":
        employee_name1 = request.POST.get("employee_name1",False)
        leave_type_nm = request.POST.get("leave_type_nm",False)
        user_auth_id = request.user.id
        data_employee = User_Management.objects.get(auth_user=user_auth_id)

        employee_name = request.POST.get("employee_name",False)
        employee_email = request.POST.get("employee_email",False)
        employee_number = request.POST.get("employee_number",False)
        employee_leave_type = request.POST.get("employee_leave_type",False)
        print("employee_leave_type1::::::::::",str(employee_leave_type))
        if  employee_leave_type == 'no':
            print("heeeeeee")
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
        absence_status = request.POST.get("absence_status",False)
        absence_category = request.POST.get("absence_category",False)

        print("request_unit_half::::",str(request_unit_half))
        if request_unit_half == "Half day":
            employee_leave_to_date = employee_leave_from_date
            pass

        


       
        request_date_from_period = request.POST.get("request_date_from_period",False)
        print("employee_leave_type::::",str(employee_leave_type))
        print("employeee_id:::::",str(data_employee.odoo_id))
        leave_apply_url = api_domain+"api/post_leave"
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
                'absence_category':absence_category
                
            }
        })

        odoo_token_data = odoo_api_request_token.objects.get(status="True")

        headers = {
            'api_key': odoo_token_data.token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }
        response1 = requests.request("POST", leave_apply_url, headers=headers, data=payload)
        print("resll::::")
        print(response1.json())
        response12 = response1.json()['result']
        
        print("response111newwwwwwwww111111::::::::::::::::::::")
        print(response12)
        l1 = response12['result']
        responsible_for_approval = ""
        try:
            responsible_for_approval = l1['responsible_for_approval'] 
        except:
            pass
        if response12['message'] == "error":

            message = response12['result']
            print("message::::::::::")
            

            print("messs:::::::")
            print(message)

            print("type::::",type(message))


            mes1 = response12['result']
            m1 = mes1[:mes1.index("\n")]
            print("m1::::")
            print(m1)

            

 
            messages.warning(request,str(m1))
            return redirect("leave_management")
        elif response12['message'] == "success":
            message = response12['result']
            print("message::::::::::")
            print(message)
            mes1 = "Your Leave from "+str(employee_leave_from_date)+" to "+str(employee_leave_to_date)+" has been submitted"

            r1 = response12['result']
            leave_id = r1['leave_id']
            leave_state = r1['state']
            print("leave_type:::::",str(leave_id))
            print("leave_state:::",str(leave_state))

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
               description =employee_leave_reason
            )
            leave_notification.save()




            try:
                check_data = User_Management.objects.get(odoo_id=int(responsible_for_approval))
                
                approval_notification =  odoo_notification(
                    notification_type="leave_approve_request",
                    message = "leave_approve_request",
                    mapping_id = int(leave_id),
                    requested_from_dt = employee_leave_from_date,
                    requested_to_dt = employee_leave_to_date,
                    read_status = 0,
                    status = leave_state,
                    auth_user_id = check_data.auth_user,
                    leave_type_name=leave_type_nm,
                    leave_apply_user_name = employee_name1,
                 description =employee_leave_reason
                )
                approval_notification.save()
                print("responsible_for_approval:::",str(responsible_for_approval))
            except:
                pass
 
            messages.success(request,str(mes1))
            return redirect("leave_management")


        

def view_all_notification(request):

    notifictaion = odoo_notification.objects.filter(auth_user_id=request.user).order_by('-id')
    update_noti = odoo_notification.objects.filter(read_status=0,auth_user_id=request.user).update(
        read_status=1
    )
    context = {
        "notifictaion":notifictaion
    }
    return render(request,'super_admin/view_all_notification.html',context)



from rest_framework.decorators import api_view
@api_view(['POST'])
def leave_status_update_api(request):
    if request.method == "POST":
        leave_id = request.POST.get("leave_id",False)
        state = request.POST.get("state",False)
        updated_data = odoo_notification.objects.filter( mapping_id = int(leave_id)).update(status=state,read_status=0)
        data = {
            'message':"success"
        }
        data_send = odoo_notification.objects.get(mapping_id= int(leave_id))
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



def view_leave_more_details(request):
    id = request.GET.get("id",False)
    print("id111111111::::::",str(id))
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
    print("resll::::")
    print(response1.json())
    response12 = response1.json()['result']
    print("ressss:::::")
    print(response12)
    r1 = response12['result'][0]
    print("new:")
    print(r1)
    emp_name = ""
    try:
        data_emp = User_Management.objects.get(auth_user=request.user)
        emp_name = data_emp.employee_name
    except :
        pass



    approve_button_status = ""
    try:
        approval_instance = odoo_notification.objects.get(mapping_id=id,auth_user_id=request.user,notification_type="leave_approve_request")
        approve_button_status = "yes"
    except:
        approve_button_status ="no"
        pass


    context = {
        'r1':r1,
        'emp_name':emp_name,
        'approve_button_status':approve_button_status
    }
    return render(request,'super_admin/view_leave_more_details.html',context)



def get_selected_employee_entitlement_balance(request):
    employee_id = request.GET.get("employee_id",False)
    print("emp_id::",str(employee_id))

    entitlement_balances_url = api_domain+"api/get_leave_entitlement"
    odoo_token_data = odoo_api_request_token.objects.get(status="True")
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




    employee_data_url =api_domain+"api/get_employee"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "employee_id": employee_id
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
    print("employee_name:::::",str(employee_name1))
    emp_registration_id = response['registration_number']
    print("emmm:::::",str(emp_registration_id))
    return render(request,'super_admin/get_selected_employee_entitlement_balance.html',{'entitlement_balances_response':entitlement_balances_response,'emp_registration_id':emp_registration_id,'employee_name1':employee_name1})





def get_child_based_leave_history(request):
    employee_id = request.GET.get("employee_id",False)
    print("employee_id1111111::::",str(employee_id))
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
        print("rs122223::::")
        
        leave_history_response12  = leave_history_response1['result']
        leave_history_response = leave_history_response12['result']
        print("r1::")
        print(leave_history_response)
        

    except:
        pass
    return render(request,'super_admin/get_child_based_leave_history.html',{'leave_history_response':leave_history_response})



def testchart(request):
    import calendar
    import datetime
    now = datetime.datetime.now()
    print(now.month)
    days = calendar.monthrange(now.year, now.month)[1]
    print("total_days::::",str(days)) 
    month_num = str(now.month)
    datetime_object = datetime.datetime.strptime(month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ",month_name)

    full_month_name = datetime_object.strftime("%B")
    print("Full name: ",full_month_name)

    employee_data = User_Management.objects.get(auth_user=request.user)

    import datetime, calendar
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    print("assss::::::")
    print(ays)

  

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
    print(now.month)
    days = calendar.monthrange(now.year, now.month)[1]
    print("total_days::::",str(days)) 
    month_num = str(now.month)
    datetime_object = datetime.datetime.strptime(month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ",month_name)

    full_month_name = datetime_object.strftime("%B")
    print("Full name: ",full_month_name)

    employee_data = User_Management.objects.get(auth_user=request.user)

    import datetime, calendar
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    print("assss::::::")
    print(ays)
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
        print("r122222::")
       
        

    except:
        pass


    print("ddddddd::::",str(get_chile_response))

    



    

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
    print("next month::::::::::::")
    from datetime import date
    y = request.GET.get("year",False)
    m = request.GET.get("month",False)
    try:
        df = date(int(y),int(m)+1,1)
    except:
        df = date(int(y)+1,int(1),1)
    new_month = df.month
    new_year = df.year
    print("new_month::::::",str(new_month))
    print("new_year:::::",str(new_year))
    
    import calendar
    import datetime
    
    days = calendar.monthrange(int(new_year), int(new_month))[1]
    print("total_days::::",str(days)) 

    month_num = str(m)
    datetime_object = datetime.datetime.strptime(str(new_month), "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ",month_name)

    full_month_name = datetime_object.strftime("%B")
    print("Full name: ",full_month_name)
    employee_data = User_Management.objects.get(auth_user=request.user)
    import datetime, calendar
    year = new_year
    month = new_month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    print("assss::::::")
    print(ays)
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
        print("r122222::")
       
        

    except:
        pass

    count1 = 0


    print("ddddddd::::",str(get_chile_response))
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
    print("next month::::::::::::")
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
    print("new_month::::::",str(new_month))
    print("new_year:::::",str(new_year))
    
    import calendar
    import datetime
    
    days = calendar.monthrange(int(new_year), int(new_month))[1]
    print("total_days::::",str(days)) 

    month_num = str(m)
    datetime_object = datetime.datetime.strptime(str(new_month), "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ",month_name)

    full_month_name = datetime_object.strftime("%B")
    print("Full name: ",full_month_name)
    employee_data = User_Management.objects.get(auth_user=request.user)
    import datetime, calendar
    year = new_year
    month = new_month
    num_days = calendar.monthrange(year, month)[1]

    ays = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    print("assss::::::")
    print(ays)
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
        print("r122222::")
       
        

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



    child_response = ""
    try:
        child_response_url = api_domain + "api/get_childs"
        child_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "employee_id": int(odoo_id)

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
    print("calllllllllllll",child_response)
    context = {




        'child_response': child_response,
        'count':len(child_response)

    }

    return render(request, 'super_admin/calendar.html', context)
    # return render(request, 'super_admin/calendar.html')
def event_depended(request):
    event_id = request.GET.get('event_id')
    print("jijijijijiii",event_id)
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
    print("resll::::")
    print(response1.json())
    response12 = response1.json()['result']
    print("ressss:::::")
    print(response12)
    r1 = response12['result'][0]
    print("new:")
    print(r1)
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
    leave_history_response = ""
    try:
        leave_history_response_url = api_domain + "api/get_leave_history_calender"
        leave_history_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {

            "employee_id" : 2834,
            "all": "True",
            "start_date" : "2022-07-01",
            "end_date" : "2022-07-31"
            }
        })
        leave_history_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers,
                                                   data=leave_history_payload).json()
        print("rs122223::::")
        print("response1::::::::")
        print(leave_history_response1)

        leave_history_response12 = leave_history_response1['result']
        leave_history_response = leave_history_response12['result']
        print("r1::")
        print(leave_history_response)


    except:
        pass
    out = []
    print(out)
    print("jiyadddddddddddddddddddddddddddd:::::::",leave_history_response)
    for event in leave_history_response:
        print("id::::::::::::",str(event['id']))
        print("date_from::",str(event['date_from']))
        print("date_to::::",str(event['date_to']))
        print(type(event['date_to']))
        from datetime import datetime
        print(datetime.fromisoformat(event['date_to']))
        df = datetime.fromisoformat(event['date_to'])
        print("date:::",str(df.date()))

        from datetime import timedelta

        date_time_obj = df+timedelta(days=1)
        print("lll")
        print(date_time_obj)

        out.append({

            'title':event['holiday_status_id'],
            'id':event['id'],
            'start': event['date_from'],
            'end': date_time_obj,
        })
        print("----nnnnnnnnnnnnnnnnnn")
    print("---------------")
    print("---out-------")
    print(out)
    print("---leave_history_response-------")
    print(leave_history_response)
    return JsonResponse(out, safe=False)


def all_events1(request):

    type1 = request.GET.get("type")
    print("type1111111111111111",type1)
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
    leave_history_response = ""
    try:
        leave_history_response_url = api_domain + "api/get_leave_history_calender"
        leave_history_payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {

            "employee_id" : 2834,
            "all": "True",
            "start_date" : "2022-07-01",
            "end_date" : "2022-07-31"
            }
        })
        leave_history_headers = {
            'api_key': odoo_token,
            'Content-Type': 'application/json',
            'Cookie': 'session_id=b53105332e1286dbd1609c81628966b3fd82110b'
        }

        leave_history_response1 = requests.request("GET", leave_history_response_url, headers=leave_history_headers,
                                                   data=leave_history_payload).json()
        print("rs122223::::")

        leave_history_response12 = leave_history_response1['result']
        leave_history_response = leave_history_response12['result']
        print("r1::")
        print(leave_history_response)


    except:
        pass
    out = []
    for event in leave_history_response:
        print("id::::::::::::", str(event['id']))
        a=event['employee_id']
        print(type(a))
        print("a::::::::::::", str(a[0]))
        print("date_from::", str(event['date_from']))
        print("date_to::::", str(event['date_to']))
        print(type(event['date_to']))
        from datetime import datetime
        print(datetime.fromisoformat(event['date_to']))
        df = datetime.fromisoformat(event['date_to'])
        print("date:::", str(df.date()))

        from datetime import timedelta

        date_time_obj = df + timedelta(days=1)
        print("lll")
        print(date_time_obj)
        print("id::::::::::::jiyad1111111", str(event['id']))
        print("type::::::::::::")
        if (str(a[0]) == type1):
            print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
            out.append({
                'title':event['holiday_status_id'],
                'id':event['id'],
                'start': event['date_from'],
                'end': date_time_obj,
            })
    print("---------------")
    return JsonResponse(out, safe=False)





def img(request):
    if request.method == "POST":
        print("heyyyy")
        n1 = request.POST.getlist('n1[]')
        print(len(n1))
        for i in range(len(n1)):
            print("hhhh")
            save = test.objects.create(
                img_path=n1[i]
            )
       
        files = request.FILES.getlist('files[]')
        print("files:::")
        print(files)
    else:
        test1 = test.objects.all()
        
        return render(request,'super_admin/img.html',{'test1':test})




def view_notification_table(request):
    notifictaion = odoo_notification.objects.filter(auth_user_id=request.user).order_by('-id')
    update_noti = odoo_notification.objects.filter(read_status=0,auth_user_id=request.user).update(
        read_status=1
    )
    context = {
        "notifictaion":notifictaion
    }
    return render(request,'super_admin/view_notification_table.html',context)