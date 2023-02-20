from django import forms
from Project_UserEmp.models import *


class empForm(forms.ModelForm):
    class Meta:
        gendel_choices = [('ชาย', 'ชาย'), ('หญิง', 'หญิง')]
        model = employee
        fields = ('id_code', 'first_name', 'sur_name', 'birthday', 'gender', 'national', 'ethnicity', 'religion',
                  'address', 'subdistrict', 'district', 'Province', 'postcode', 'tel', 'email', 'appointment',
                  'department', 'username', 'password', 'img_profile')
        widgets = {
            'id_code': forms.TextInput(attrs={'max_length': '13', 'min_length': '13','class': 'form-control', 'pattern': "[0-9]+",'required': 'required'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'max_length': '255',}),
            'sur_name': forms.TextInput(attrs={'class': 'form-control', 'max_length': '255',}),
            'national': forms.TextInput(attrs={'class': 'form-control', 'max_length': '100',}),
            'ethnicity': forms.TextInput(attrs={'class': 'form-control', 'max_length': '100',}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'max_length': '100',}),
            'subdistrict': forms.TextInput(attrs={'class': 'form-control', 'max_length': '100',}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'max_length': '100',}),
            'Province': forms.TextInput(attrs={'class': 'form-control', 'max_length': '100',}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'pattern': "[0-9]+",'max_length': '5',}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'pattern': "[0-9]+",'max_length': '10',}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'max_length': '100',}),
            'username': forms.TextInput(attrs={'class': 'form-control','max_length': '100',}),
            'birthday': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'gender': forms.RadioSelect(choices=gendel_choices, attrs={'class': 'form-check-input', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'appointment': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required', 'minlength': '8', 'maxlength': '32'}),
            'img_profile': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'onchange': 'readimg(this)'}),
        }
        labels = {
            'id_code': 'รหัสบัตรประจำตัวประชาชน',
            'first_name': 'ชื่อ',
            'sur_name': 'นามสกุล',
            'birthday': 'วัน/เดือน/ปี เกิด',
            'gender': 'เพศ',
            'national': 'สัญชาติ',
            'ethnicity': 'เชื้อชาติ',
            'religion': 'ศาสนา',
            'address': 'ที่อยู่',
            'subdistrict': 'ตำบล',
            'district': 'อำเภอ',
            'Province': 'จังหวัด',
            'postcode': 'รหัสไปรษณีย์',
            'tel': 'เบอร์โทรศัพท์',
            'email': 'Email',
            'appointment': 'ตำแหน่ง',
            'department': 'แผนก',
            'username': 'ชื่อผู้ใช้',
            'password': 'รหัสผ่าน',
            'img_profile': 'รูป',
        }


    def updateForm(self):
        self.fields['id_code'].widget.attrs['readonly'] = True
        self.fields['password'].widget.attrs['hidden'] = True
class appointmentForm(forms.ModelForm):
    List_bool = [('True', 'เปิด'), ('False', 'ปิด')]
    app_status = forms.TypedChoiceField(choices=List_bool,widget=forms.RadioSelect)
    class Meta:
        model = appointment
        fields = ('app_name','app_permission','app_status')
        widgets ={
            'app_name':forms.TextInput(attrs={'class':'form-control','maxlength':100}),
            'app_permission':forms.TextInput(attrs={'class':'form-control','maxlength':10,'pattern': "[0-9]+"}),

        }
        labels = {
            'app_name':'ชื่อตำแหน่ง',
            'app_permission':'ระดับการใช้งานระบบ',
            'app_status':'สถานะการเปิดใช้งานตำแหน่ง',
        }
class departmentForm(forms.ModelForm):
    List_bool = [('True', 'เปิด'), ('False', 'ปิด')]
    dep_status = forms.TypedChoiceField(choices=List_bool, widget=forms.RadioSelect,label="สถานะการเปิดใช้งาน")
    class Meta:
        model = department
        fields = ('dep_name','dep_status')
        widgets = {
            'dep_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
        }
        labels = {
            'dep_name':'ชื่อแผนก',
        }
class tooltypeForm(forms.ModelForm):
    List_bool = [('True', 'เปิด'), ('False', 'ปิด')]
    tooly_status = forms.TypedChoiceField(choices=List_bool, widget=forms.RadioSelect,label="สถานะการเปิดใช้งาน")
    class Meta:
        model = tooltype
        fields = ('tooly_name','tooly_des','tooly_status')
        widgets = {
            'tooly_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'tooly_des': forms.Textarea(attrs={'class': 'form-control', 'row': 2}),
        }
        labels = {
            'tooly_name':'ชื่อประเภทเครื่องมือช่าง / อุปกรณ์ทั้งหมด',
            'tooly_des':'คำอธิบายประเภท'
        }
class toolForm(forms.ModelForm):
    class Meta:
        model = tool
        fields = ('tool_name','tool_price','tool_type','tool_des','tool_img')
        widgets = {
            'tool_name':forms.TextInput(attrs={'class':'form-control','maxlength':'100'}),
            'tool_price':forms.NumberInput(attrs={'class':'form-control',}),
            'tool_type':forms.Select(attrs={'class':'form-control'}),
            'tool_des':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'tool_img':forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'onchange': 'readimg(this)'})
        }
        labels = {
            'tool_name':'ชื่อ',
            'tool_price':'ราคา',
            'tool_type':'ประเภท',
            'tool_des':'คำอธิบาย',
            'tool_img':'รูปภาพ',
        }