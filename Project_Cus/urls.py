from django.urls import path

from Project_Cus import views

urlpatterns = [
    path('', views.homepage, name='cus_home'),
    path('home', views.homepage, name='cus_home'),
    path('register', views.register, name='cus_register'),
    path('repair/form', views.repair_form, name='cus_repair_form'),
]
