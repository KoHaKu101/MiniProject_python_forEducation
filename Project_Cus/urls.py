from django.urls import path

from Project_Cus import views

urlpatterns = [
    path('', views.homepage, name='cus_home'),
    path('home', views.homepage, name='cus_home'),
    path('login', views.login, name='cus_login'),
    path('logout', views.logout, name='cus_logout'),
    path('register', views.register, name='cus_register'),
    path('repair/form', views.repair_form, name='cus_repair_form'),
    path('repair/list', views.repair_list, name='cus_repair_list'),
    path('checkout/<order_id>', views.check_out, name='checkout'),
    path('pay/<order_rec_id>', views.check_out_qrcode, name='check_out_qrcode'),
    path('successcheckout/<order_rec_id>', views.check_out_success, name='check_out_success'),
]
