from django import views
from django.contrib import admin
from django.urls import path,include
from . import views

from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [

    path('',views.index,name='index'),
    path('login_action',views.login_action,name='login_action'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('admin_add_user',views.admin_add_user,name='admin_add_user'),
    path('menu',views.menu,name='menu'),
    path('admin_add_user_action',views.admin_add_user_action,name='admin_add_user_action'),
    path('admin_view_user',views.admin_view_user,name='admin_view_user'),
    path('admin_delete_user_action',views.admin_delete_user_action,name='admin_delete_user_action'),
    path('admin_edit_user_details_action',views.admin_edit_user_details_action,name='admin_edit_user_details_action'),
    path('admin_inactive_user_action',views.admin_inactive_user_action,name='admin_inactive_user_action'),
    path('admin_active_user_action',views.admin_active_user_action,name='admin_active_user_action'),
    path('logout',auth_views.LogoutView.as_view(),name="logout"),
    path('index',views.index,name='index'),
    path('login_page',views.index,name='login_page'),
    path('user_home',views.user_home,name='user_home'),
    path('user_apply_leave_management',views.user_apply_leave_management,name='user_apply_leave_management'),
    path('user_apply_leave_action',views.user_apply_leave_action,name='user_apply_leave_action'),
    path('user_apply_petty_cash',views.user_apply_petty_cash,name='user_apply_petty_cash'),
    path('user_apply_advance_salary_request_from',views.user_apply_advance_salary_request_from,name='user_apply_advance_salary_request_from'),
    path('user_view_leave_request',views.user_view_leave_request,name='user_view_leave_request'),
    path('user_view_petty_cash',views.user_view_petty_cash,name='user_view_petty_cash'),
    path('user_view_advance_salary',views.user_view_advance_salary,name='user_view_advance_salary'),



    # -----------new url --------------

    path('role_management',views.role_management,name='role_management'),
    path('add_role_action',views.add_role_action,name='add_role_action'),
    path('view_role_more_details',views.view_role_more_details,name='view_role_more_details'),
    path('edit_role_details',views.edit_role_details,name='edit_role_details'),
    path('edit_role_details_action',views.edit_role_details_action,name='edit_role_details_action'),
    path('view_company_details',views.view_company_details,name='view_company_details'),
    path('employee_master',views.employee_master,name='employee_master'),
    path('employee_more_details',views.employee_more_details,name='employee_more_details'),
    path('user_management',views.user_management,name='user_management'),
    path('getemployee_branch_dpt',views.getemployee_branch_dpt,name='getemployee_branch_dpt'),
    path('user_add_action',views.user_add_action,name='user_add_action'),
    path('view_user_more_details',views.view_user_more_details,name='view_user_more_details'),
    path('edit_user_more_details',views.edit_user_more_details,name='edit_user_more_details'),
    path('edit_user_details_action',views.edit_user_details_action,name='edit_user_details_action'),
    path('update_user_role_permission_action',views.update_user_role_permission_action,name='update_user_role_permission_action'),
    path('user_role_delete_action',views.user_role_delete_action,name='user_role_delete_action'),
    path('user_add_new_role_action',views.user_add_new_role_action,name='user_add_new_role_action'),
    path('leave_management',views.leave_management,name='leave_management'),
    path('get_total_available_leave_count',views.get_total_available_leave_count,name='get_total_available_leave_count'),
    path('petty_cash_management',views.petty_cash_management,name='petty_cash_management'),
    path('advance_salary_management',views.advance_salary_management,name='advance_salary_management'),
    path('role_edit_modal_function',views.role_edit_modal_function,name='role_edit_modal_function'),
    path('user_edit_modal_function',views.user_edit_modal_function,name='user_edit_modal_function'),
    path('user_role_log_modal',views.user_role_log_modal,name='user_role_log_modal'),
    path('user_leave_apply_action',views.user_leave_apply_action,name='user_leave_apply_action'),
    path('view_all_notification',views.view_all_notification,name='view_all_notification'),
    path('view_leave_more_details',views.view_leave_more_details,name='view_leave_more_details'),
    path('get_selected_employee_entitlement_balance',views.get_selected_employee_entitlement_balance,name='get_selected_employee_entitlement_balance'),
    path('get_child_based_leave_history',views.get_child_based_leave_history,name='get_child_based_leave_history'),
    path('user_leave_gantt_chart',views.user_leave_gantt_chart,name='user_leave_gantt_chart'),
    path('user_leave_gantt_chart_next_month_action',views.user_leave_gantt_chart_next_month_action,name='user_leave_gantt_chart_next_month_action'),
    path('user_leave_gantt_chart_prev_month_action',views.user_leave_gantt_chart_prev_month_action,name='user_leave_gantt_chart_prev_month_action'),
    path('calendar', views.calendar, name='calendar'),
   
   
    path('login_page1',views.login_page1,name='login_page1'),
    path('view_notification_table',views.view_notification_table,name='view_notification_table'),
    path('leave_approve_action',views.leave_approve_action,name='leave_approve_action'),
    path('reject_leave_request_action',views.reject_leave_request_action,name='reject_leave_request_action'),
    path('leave_reassign_action',views.leave_reassign_action,name='leave_reassign_action'),
    path('user_fcmtoken_save',views.user_fcmtoken_save,name='user_fcmtoken_save'),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    # ---------odoo api and authentication function 
    path('odoo_login_api',obtain_auth_token,name='odoo_login_api'),
    path('leave_create_api',views.leave_create_api.as_view(),name='leave_create_api'),
    path('odoo_leave_status_update_api',views.odoo_leave_status_update_api.as_view(),name='odoo_leave_status_update_api'),
    path('depended', views.depended,name='depended'),
    path('leave_calendar', views.leave_calendar, name='leave_calendar'),
    path('event_depended', views.event_depended, name='event_depended'),
    path('all_events', views.all_events, name='all_events'),
    path('employee_events', views.employee_events, name='employee_events'),
    path('cal_depended', views.cal_depended,name='cal_depended'),

    path('username_exists_condition',views.username_exists_condition,name='username_exists_condition'),

    path('user_login_log',views.user_login_log,name='user_login_log'),
    path('user_login_log_date_filter_action',views.user_login_log_date_filter_action,name='user_login_log_date_filter_action'),
    path('role_exists_check',views.role_exists_check,name='role_exists_check'),


    path('test_gantt_chart',views.test_gantt_chart,name='test_gantt_chart'),

    path('test_file_upload_ajax',views.test_file_upload_ajax,name='test_file_upload_ajax'),

    




 



    
    

    
    
    
    


    path("test_api",views.test_api,name='test_api'),
    



    path("test_update_auth_user_table",views.test_update_auth_user_table,name='test_update_auth_user_table'),
    path('test_r1',views.test_r1,name='test_r1'),
    path('testr1',views.testr1,name='testr1'),

    path("leave_status_update_api",views.leave_status_update_api,name='leave_status_update_api'),

    path('test_r1',views.test_r1,name='test_r1'),
    path('test_r2',views.test_r2,name='test_r2'),
    path('testchart',views.testchart,name='testchart'),
    path('img',views.img,name='img'),
    path('loader',views.loader,name='loader'),
    path('test_current_address',views.test_current_address,name='test_current_address'),

    
    
    

    

    




]