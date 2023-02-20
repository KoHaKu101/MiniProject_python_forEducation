import datetime

from django.db import models
from Project_UserEmp.models import *
# Create your models here.
class customer(models.Model):
    cus_id = models.CharField(max_length=10,primary_key=True)
    first_name = models.CharField(max_length=255,null=False)
    sur_name = models.CharField(max_length=255,null=False)
    birthday = models.DateField(null=False)
    address = models.TextField(null=True,default='')
    subdistrict = models.CharField(max_length=100,null=False)
    district = models.CharField(max_length=100,null=False)
    Province = models.CharField(max_length=100,null=False)
    postcode = models.CharField(max_length=20,null=False)
    tel = models.CharField(max_length=10,null=False)
    email = models.CharField(max_length=100,null=False,unique=True)
    password = models.CharField(max_length=32,null=False)
class order(models.Model):
    order_id = models.CharField(max_length=10,primary_key=True)
    title = models.CharField(max_length=255,null=False)
    desc = models.TextField(null=False,default='')
    tel_order = models.CharField(max_length=10,null=False)
    cus = models.ForeignKey(customer,on_delete=models.CASCADE,default=None)
    order_img = models.ImageField(upload_to="static/images/orders/",null=False,default="")
    order_status = models.IntegerField(null=False,default=0)
    create_date_time = models.CharField(null=True,default="",blank=True,max_length=50)
    submit_date_time = models.CharField(null=True,default="",blank=True,max_length=50)
    submit_emp = models.ForeignKey(employee,on_delete=models.CASCADE,default=None,null=True,blank=True)