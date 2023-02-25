from django import forms
from Project_Cus.models import *
from Project_UserEmp.models import *

class customerForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ('first_name', 'sur_name', 'birthday', 'tel', 'email','password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '255','placeholder':'ชื่อ'}),
            'sur_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '255','placeholder':'นามสกุล'}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'pattern': "[0-9]+",'minlength':'10','maxlength': '10','placeholder':'เบอร์โทรศัพท์'}),
            'birthday': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': '100','placeholder':'อีเมล์'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required', 'minlength': '8', 'maxlength': '32','placeholder':'รหัสผ่าน'}),
        }
        labels = {
            'first_name': 'ชื่อ',
            'sur_name': 'นามสกุล',
            'tel': 'เบอร์โทรศัพท์',
            'birthday':'วัน เดือน ปี เกิด',
            'email': 'Email',
            'password': 'รหัสผ่าน',
        }


    def updateForm(self):
        self.fields['id_code'].widget.attrs['readonly'] = True
        self.fields['password'].widget.attrs['hidden'] = True
class orderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ('title', 'desc', 'tel_order','order_img')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '255','placeholder':'ชื่อหัวข้อ'}),
            'desc': forms.Textarea(attrs={'class': 'form-control','rows':6}),
            'tel_order': forms.TextInput(attrs={'class': 'form-control', 'pattern': "[0-9]+",'minlength':'10','maxlength': '10','placeholder':'เบอร์โทรศัพท์'}),
            'order_img': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'onchange': 'readimg(this)'}),
        }
        labels = {
            'title': 'ชื่อ',
            'desc': 'นามสกุล',
            'tel': 'เบอร์โทรศัพท์',
        }

class addresssForm(forms.ModelForm):
    class Meta:
        model = cus_address
        fields = ('first_name','sur_name','address','subdistrict','district','province','postcode','tel','email','note')
        widgets = {
            'first_name':forms.TextInput(attrs={'class': 'form-control', 'maxlength': '255'}),
            'sur_name':forms.TextInput(attrs={'class': 'form-control', 'maxlength': '255'}),
            'subdistrict':forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'district':forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'province':forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'postcode':forms.TextInput(attrs={'class': 'form-control', 'pattern': "[0-9]+",'maxlength': '5',}),
            'tel':forms.TextInput(attrs={'class': 'form-control', 'pattern': "[0-9]+",'maxlength': '10',}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'note':forms.Textarea(attrs={'class': 'form-control','rows':3}),
            'address':forms.Textarea(attrs={'class': 'form-control','rows':3}),
        }
class payForm(forms.ModelForm):
    class Meta:
        model = order_payment
        fields = ('pay_img',)
        widgets = {
            'pay_img':forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'onchange': 'readimg(this)','required':'required'})
        }




