from django.urls import path

from Project_UserEmp import views

urlpatterns = [
    path('', views.emp_home, name='emp_home'),
    path('login', views.emp_login, name='emp_login'),

    path('list/emp', views.list_emp, name='list_emp'),
    path('add/emp', views.add_emp, name='add_emp'),
    path('update/emp/<id>', views.update_emp, name='update_emp'),
    path('delete/emp/<id>', views.delete_emp, name='deleate_emp'),

    path('list/tool', views.list_tool, name='list_tool'),
    path('add/tool', views.add_tool, name='add_tool'),
    path('update/tool/<tool_id>', views.update_tool, name='update_tool'),
    path('delete/tool/<tool_id>', views.delete_tool, name='deleate_tool'),

    path('list/order', views.list_order, name='list_emp_order'),
    path('view/order/<order_id>', views.view_order, name='view_emp_order'),
    path('check/order/<order_id>', views.check_order, name='check_emp_order'),
    path('receive/order/<order_id>', views.receive_order, name='receive_emp_order'),
    path('cancel/order/<order_id>', views.cancel_order, name='cancel_emp_order'),

    path('list/payment', views.pay_confirm_list, name='list_payment'),
    path('view/payment/<order_rec_id>', views.pay_detail, name='pay_detail'),
    path('confirm/payment/<order_rec_id>', views.pay_confirm, name='pay_confirm'),

    path('setting/list/appointment', views.list_appointment, name='list_appoinment'),
    path('setting/add/appointment', views.add_appointment, name='add_appoinment'),
    path('setting/update/appointment/<app_id>', views.update_appointment, name='update_appointment'),
    path('setting/delete/appointment/<app_id>', views.delete_appointment, name='delete_appointment'),

    path('setting/list/department', views.list_department, name='list_department'),
    path('setting/add/department', views.add_department, name='add_department'),
    path('setting/update/department/<dep_id>', views.update_department, name='update_department'),
    path('setting/delete/department/<dep_id>', views.delete_department, name='delete_department'),

    path('setting/list/tooltype', views.list_tooltype, name='list_tooltype'),
    path('setting/add/tooltype', views.add_tooltype, name='add_tooltype'),
    path('setting/update/tooltype/<tooly_id>', views.update_tooltype, name='update_tooltype'),
    path('setting/delete/tooltype/<tooly_id>', views.delete_tooltype, name='delete_tooltype'),

    path('setting/default', views.setting, name='setting'),
    path('report/pay/<order_rec_id>',views.report,name="report_pay")
]
