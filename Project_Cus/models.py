
from django.db import models

class customer(models.Model):
    cus_id = models.CharField(max_length=10,primary_key=True)
    first_name = models.CharField(max_length=255,null=False)
    sur_name = models.CharField(max_length=255,null=False)
    birthday = models.DateField(null=False)
    tel = models.CharField(max_length=10,null=False)
    email = models.CharField(max_length=100,null=False,unique=True)
    password = models.CharField(max_length=32,null=False)
class cus_address(models.Model):
    cus_add = models.CharField(max_length=10,primary_key=True)
    cus = models.ForeignKey(customer,on_delete=models.PROTECT,null=False)
    first_name = models.CharField(max_length=255, null=False)
    sur_name = models.CharField(max_length=255, null=False)
    address = models.TextField(null=False)
    subdistrict = models.CharField(max_length=100, null=False)
    district = models.CharField(max_length=100, null=False)
    province = models.CharField(max_length=100, null=False)
    postcode = models.CharField(max_length=20, null=False)
    tel = models.CharField(max_length=10, null=False)
    email = models.CharField(max_length=100, null=False)
    note = models.TextField(null=True,default="",blank=True)


