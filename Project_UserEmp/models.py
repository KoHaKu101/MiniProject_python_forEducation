from django.db import models


class appointment(models.Model):
    app_id = models.CharField(max_length=10,primary_key=True)
    app_name = models.CharField(max_length=100,unique=True)
    app_permission = models.CharField(max_length=10,null=False,default="1")
    app_status = models.BooleanField(null=False,default='True')
    def __str__(self):
        return  self.app_name
class department(models.Model):
    dep_id = models.CharField(max_length=10,primary_key=True)
    dep_name = models.CharField(max_length=100,unique=True)
    dep_status = models.BooleanField(null=False,default='True')
    def __str__(self):
        return  self.dep_name
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
    tool_price = models.BooleanField(null=False,default='True')
    tool_type = models.ForeignKey(tooltype,on_delete=models.CASCADE,default=None)
    tool_des = models.TextField(null=True, blank=True, default="")
    tool_img = models.ImageField(upload_to="static/images/employee/",blank=True, null=True,default="")
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
    appointment = models.ForeignKey(appointment,on_delete=models.CASCADE,default=None)
    department = models.ForeignKey(department,on_delete=models.CASCADE,default=None)
    username = models.CharField(max_length = 100,null=False)
    password = models.CharField(max_length=32,null=False)
    img_profile = models.ImageField(upload_to="static/images/employee/",blank=True, null=True,default="")


