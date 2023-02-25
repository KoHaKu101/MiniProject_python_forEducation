from django.db import models
from django.db.models import ProtectedError
from Project_Cus.models import customer

class appointment(models.Model):
    app_id = models.CharField(max_length=10,primary_key=True)
    app_name = models.CharField(max_length=100,unique=True)
    app_permission = models.CharField(max_length=10,null=False,default="1")
    app_status = models.BooleanField(null=False,default='True')
    def __str__(self):
        return  self.app_name
class department(models.Model):
    dep_id = models.CharField(max_length=10,primary_key=True)
    dep_name_th = models.CharField(max_length=100,unique=True)
    dep_name_en = models.CharField(max_length=100, unique=True)
    dep_status = models.BooleanField(null=False,default='True')
    def __str__(self):
        return  self.dep_name_th
class tooltype(models.Model):
    tooly_id = models.CharField(max_length=10,primary_key=True)
    tooly_name = models.CharField(max_length=100,unique=True)
    tooly_status = models.BooleanField(null=False,default='True')
    tooly_des = models.TextField(null=True,blank=True,default="")
    def __str__(self):
        return self.tooly_name
class tool(models.Model):
    tool_id = models.CharField(max_length=10,primary_key=True)
    tool_name = models.CharField(max_length=100,unique=True)
    tool_price = models.FloatField(default=0.00,null=False)
    tool_type = models.ForeignKey(tooltype,on_delete=models.PROTECT,default=None)
    tool_des = models.TextField(null=True, blank=True, default="")
    tool_img = models.ImageField(upload_to="static/images/tool/",default="")

class employee(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    id_code = models.CharField(max_length=13,unique=True)
    first_name = models.CharField(max_length=255,null=False)
    sur_name = models.CharField(max_length=255,null=False)
    birthday = models.DateField(null=False)
    gender = models.CharField(max_length=20,null=False)
    national = models.CharField(max_length=100,null=False)
    ethnicity = models.CharField(max_length=100,null=False)
    religion = models.CharField(max_length=100,null=False)
    address = models.TextField(null=True,default='')
    subdistrict = models.CharField(max_length=100,null=False)
    district = models.CharField(max_length=100,null=False)
    Province = models.CharField(max_length=100,null=False)
    postcode = models.CharField(max_length=20,null=False)
    tel = models.CharField(max_length=10,null=False)
    email = models.CharField(max_length=100,null=False)
    appointment = models.ForeignKey(appointment,on_delete=models.PROTECT,default=None)
    department = models.ForeignKey(department,on_delete=models.PROTECT,default=None)
    username = models.CharField(max_length = 100,null=False)
    password = models.CharField(max_length=32,null=False)
    img_profile = models.ImageField(upload_to="static/images/employee/",blank=True, null=True,default="")

class order(models.Model):
    order_id = models.CharField(max_length=10,primary_key=True)
    title = models.CharField(max_length=255,null=False)
    desc = models.TextField(null=False,default='')
    tel_order = models.CharField(max_length=10,null=False)
    cus = models.ForeignKey(customer,on_delete=models.PROTECT,default=None)
    order_img = models.ImageField(upload_to="static/images/orders/",null=False,default="")
    order_status = models.IntegerField(null=False,default=0)
    create_date_time = models.CharField(null=False,max_length=50)
    submit_date_time = models.CharField(null=True,default="",blank=True,max_length=50)
    submit_emp = models.ForeignKey(employee,on_delete=models.PROTECT,default=None,null=True,blank=True)
class order_receive(models.Model):
    order_rec_id = models.CharField(max_length=10,primary_key=True)
    order = models.ForeignKey(order,on_delete=models.PROTECT,null=False)
    emp = models.ForeignKey(employee,on_delete=models.PROTECT,null=False)
    price = models.FloatField(default=0.00,null=True,blank=True)
    price_service = models.FloatField(default=0.00, null=True, blank=True)
    price_total = models.FloatField(default=0.00, null=True, blank=True)
    order_rec_date = models.CharField(null=False,max_length=50)
    order_rec_status = models.CharField(max_length=1,default="1")

class order_queue(models.Model):
    order_que_id = models.CharField(max_length=10,primary_key=True)
    order_receive = models.ForeignKey(order_receive,on_delete=models.PROTECT,null=False)
    order_que_number = models.IntegerField(default=1,null=False)
    order_que_date = models.CharField(null=False,max_length=50)
    order_que_status = models.CharField(max_length=1,default="1")
class repair_detail(models.Model):
    re_id = models.CharField(max_length=10, primary_key=True)
    order_receive = models.ForeignKey(order_receive, on_delete=models.PROTECT, null=False,unique=True)
    emp = models.ForeignKey(employee, on_delete=models.PROTECT, null=False)
    re_detail = models.TextField(null=False)
    re_date_start = models.CharField(null=True, default="", blank=True, max_length=50)
    re_date_end = models.CharField(null=True, default="", blank=True, max_length=50)

class tool_use(models.Model):
    tu_id = models.CharField(max_length=10, primary_key=True)
    tool = models.ForeignKey(tool, on_delete=models.PROTECT, null=False)
    order_receive = models.ForeignKey(order_receive, on_delete=models.PROTECT, null=False)
    tu_total_price = models.FloatField(default=0.00,null=False)
    tu_amount = models.IntegerField(default=1,null=False)
    tu_get_date = models.CharField(null=False,max_length=50)
class setting_default(models.Model):
    set_id = models.CharField(max_length=10, primary_key=True)
    service_paid = models.FloatField(default=200.00,null=False)
    line_notify = models.CharField(null=True,blank=True,max_length=100,default="")
class order_payment(models.Model):
    pay_id = models.CharField(max_length=10,primary_key=True)
    order_rec = models.ForeignKey(order_receive,on_delete=models.PROTECT,null=False,unique=True)
    pay_type = models.CharField(null=False,max_length=1)
    pay_img = models.ImageField(upload_to="static/images/pay/",null=True,blank=True,default="")
    pay_status = models.CharField(null=False,max_length=1)
    pay_date_send = models.CharField(null=True,max_length=50,blank=True,default="")
    pay_date_check = models.CharField(null=True,max_length=50,blank=True,default="")

