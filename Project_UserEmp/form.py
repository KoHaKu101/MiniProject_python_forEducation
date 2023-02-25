from django import forms
from Project_UserEmp.models import *


class empForm(forms.ModelForm):
    class Meta:
        gendel_choices = [('ชาย', 'ชาย'), ('หญิง', 'หญิง')]
        model = employee
        fields = ('id_code', 'first_name', 'sur_name', 'birthday', 'gender', 'national', 'ethnicity', 'religion',
                  'address', 'subdistrict', 'district', 'Province', 'postcode', 'tel', 'email', 'appointment',
                  'department', 'username', 'img_profile')
        widgets = {
            'id_code': forms.TextInput(attrs={'minlength': '13','maxlength': '13', 'class': 'form-control', 'pattern': "[0-9]+",'required': 'required'}),
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
            'email': forms.EmailInput(attrs={'class': 'form-control', 'max_length': '100'}),
            'username': forms.TextInput(attrs={'class': 'form-control','max_length': '100',}),
            'birthday': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'}),
            'gender': forms.RadioSelect(choices=gendel_choices, attrs={'class': 'form-check-input', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'appointment': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
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
            'img_profile': 'รูป',
        }


    def updateForm(self):
        self.fields['id_code'].widget.attrs['readonly'] = True

class appointmentForm(forms.ModelForm):
    class Meta:
        model = appointment
        fields = ('app_name',)
        widgets ={
            'app_name':forms.TextInput(attrs={'class':'form-control','maxlength':100}),
        }
        labels = {
            'app_name':'ชื่อตำแหน่ง',
        }
class departmentForm(forms.ModelForm):
    class Meta:
        model = department
        fields = ('dep_name_th','dep_name_en')
        widgets = {
            'dep_name_th': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100,'require':'require'}),
            'dep_name_en': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100,'require':'require'}),
        }
        labels = {
            'dep_name_th':'ชื่อแผนก (ไทย)',
            'dep_name_en': 'ชื่อแผนก (อังกฤษ)',
        }
class tooltypeForm(forms.ModelForm):
    # List_bool = [('True', 'เปิด'), ('False', 'ปิด')]
    # tooly_status = forms.TypedChoiceField(choices=List_bool, widget=forms.RadioSelect,label="สถานะการเปิดใช้งาน")
    class Meta:
        model = tooltype
        fields = ('tooly_name','tooly_des')
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

class orderReceiveForm(forms.ModelForm):
    class Meta:
        model = order_receive
        fields = ()
class orderQueueForm(forms.ModelForm):
    class Meta:
        model = order_queue
        fields = ()
class repairDetailFrom(forms.ModelForm):
    class Meta:
        model = repair_detail
        fields = ('re_detail','re_date_start','re_date_end')
        widgets = {
            're_detail':forms.Textarea(attrs={'class':'form-control','rows':'4'}),
            're_date_start':forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'}),
            're_date_end':forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'}),

        }
        labels = {
            're_detail':'ชื่อ',
            're_date_start':'ราคา',
            're_date_end':'ประเภท',
        }
    def updateForm(self):
        self.fields['re_detail'].widget.attrs['readonly'] = True
        self.fields['re_date_start'].widget.attrs['readonly'] = True
        self.fields['re_date_end'].widget.attrs['readonly'] = True

class toolUseForm(forms.ModelForm):
    class Meta:
        model = tool_use
        fields = ()

class settingForm(forms.ModelForm):
    class Meta:
        model = setting_default
        fields = ('service_paid', 'line_notify')
        widgets = {
            'service_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'line_notify': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'service_paid': 'ชื่อ',
            'line_notify': 'ราคา',
        }