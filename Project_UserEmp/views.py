import os

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import *
from .form import *
# Create your views here.
def emp_home(request):
    return render(request, 'userEmployee/home.html')
def list_emp(requset):
    data = employee.objects.all().order_by('id')
    context = {'data':data}
    return render(requset, 'userEmployee/list/emp.html', context)
def add_emp(request):
    if request.method == "POST":
        form = empForm(data = request.POST, files=request.FILES or None)
        if form.is_valid():
            get_form = form.save(commit=False)
            id = employee.objects.values_list('id', flat=True).last()
            if id is None:
                emp_id = 'emp_000001'
            else:
                str_id = str(id)
                position_id_number = str_id.rfind("_")+1
                str_id = str_id[position_id_number:10]
                number_id = int(str_id) + 1
                number_len = len(str_id) - len(str(number_id))
                id_first = 'emp_'
                for number_1 in range(0, number_len):
                    id_first = id_first + '0'
                emp_id = id_first + str(number_id)

            filepath = get_form.img_profile.name
            if filepath is not None:
                filepath = get_form.img_profile.name
                position_number = filepath.rfind('.')
                ext = filepath[position_number:]

                filepath_name = filepath.split('/')
                old_name = filepath_name[len(filepath_name) - 1]
                new_name = emp_id + ext
                get_form.id = emp_id
                get_form.save()

                emp = get_object_or_404(employee, id=emp_id)
                emp.img_profile.name = '/images/employee/' + new_name
                emp.save()

                if os.path.exists('static/images/employee/' + new_name):
                    os.remove('static/images/employee/' + new_name)
                os.rename('static/images/employee/' + old_name, 'static/images/employee/' + new_name)
            else:
                get_form.id = emp_id
                get_form.save()
            return redirect('list_emp')
    else:
        form = empForm()
    context = {'form': form}
    return render(request,'userEmployee/insert/emp.html',context)
def update_emp(request,id):
    employee_data = get_object_or_404(employee, id=id)
    img_profile = employee_data.img_profile.name
    if request.method == 'POST':
        form = empForm(data=request.POST or None,files=request.FILES or None,instance=employee_data)
        if form.is_valid() :
            get_form = form.save(commit=False)

            if get_form.img_profile.name != img_profile:
                emp_id = get_form.id
                filepath = get_form.img_profile.name
                position_number = filepath.rfind('.')
                ext = filepath[position_number:]

                filepath_name = filepath.split('/')
                old_name = filepath_name[len(filepath_name) - 1]
                new_name = emp_id + ext
                get_form.save()

                emp = get_object_or_404(employee, id=emp_id)
                emp.img_profile.name = '/images/employee/' + new_name
                emp.save()

                if os.path.exists('static/images/employee/' + new_name):
                    os.remove('static/images/employee/' + new_name)
                os.rename('static/images/employee/' + old_name, 'static/images/employee/' + new_name)
                return redirect('updateemp',id = id)
            else:

                get_form.save()
                return redirect('updateemp',id = id)
        else:
            form = empForm(instance=employee_data)
    else:
        form = empForm(instance=employee_data)
    form.updateForm()
    context = {'form' : form,'img_profile' : img_profile,'id':id}
    return render(request,'userEmployee/update/emp.html',context)
def delete_emp(request,id):
    emp_data = get_object_or_404(employee, id=id)
    if emp_data.img_profile == '':
        emp_data.delete()
    else:
        os.remove('static/' + emp_data.img_profile.name)
        emp_data.delete()
    return redirect('list_emp')
def list_appointment(request):
    data = appointment.objects.all().order_by("app_permission")
    context = {'context':data}
    return  render(request, 'userEmployee/list/appointment.html', context)
def add_appointment(request):
    if request.method == 'POST':
        form = appointmentForm(data=request.POST)
        if form.is_valid():
            get_form = form.save(commit=False)
            # เพิ่มที่ละเลข
            id = appointment.objects.values_list('app_id', flat=True).last()
            if id in None:
                app_id = 'app_000001'
            else:
                str_id = str(id)
                position_id_number = str_id.rfind("_")+1
                str_id = str_id[position_id_number:10]
                number_id = int(str_id) + 1
                number_len = len(str_id) - len(str(number_id))
                id_first = 'app_'
                for number_1 in range(0,number_len):
                    id_first = id_first + '0'
                app_id = id_first+str(number_id)
            # จบเพิ่มที่ละเลข
            get_form.app_id = app_id
            get_form.save()
            return redirect('list_appoinment')

    else:
        form = appointmentForm()
    context = {'form':form}
    return render(request,'userEmployee/insert/appointment.html',context)
def update_appointment(request,app_id):
    appointment_data = get_object_or_404(appointment, app_id=app_id)
    if request.method == 'POST':
        form = appointmentForm(data=request.POST,instance=appointment_data)
        if form.is_valid():
            form.save()
            return redirect('list_appoinment')
    else:
        form = appointmentForm(instance = appointment_data)
    context = {'form':form,'app_id':app_id}
    return render(request,'userEmployee/update/appointment.html',context)
def delete_appointment(request,app_id):
    appointment_data = get_object_or_404(appointment, app_id=app_id)
    appointment_data.delete()
    return redirect('list_appoinment')

def list_department(request):
    department_data = department.objects.all().order_by("dep_id")
    context = {'context':department_data}
    return  render(request, 'userEmployee/list/department.html', context)
def add_department(request):
    if request.method == 'POST':
        form = departmentForm(data=request.POST)
        if form.is_valid():
            get_form = form.save(commit=False)
            # เพิ่มที่ละเลข
            id = department.objects.values_list('dep_id', flat=True).last()
            if id is None:
                dep_id = 'dep_000001'
            else:
                str_id = str(id)
                position_id_number = str_id.rfind("_")+1
                str_id = str_id[position_id_number:10]
                number_id = int(str_id) + 1
                number_len = len(str_id) - len(str(number_id))
                id_first = 'dep_'
                for number_1 in range(0,number_len):
                    id_first = id_first + '0'
                dep_id = id_first+str(number_id)
            # จบเพิ่มที่ละเลข
            get_form.dep_id = dep_id
            get_form.save()
            return redirect('list_department')

    else:
        form = departmentForm()
    context = {'form':form}
    return render(request,'userEmployee/insert/department.html',context)
def update_department(request,dep_id):
    department_data = get_object_or_404(department, dep_id=dep_id)
    if request.method == 'POST':
        form = departmentForm(data=request.POST,instance=department_data)
        if form.is_valid():
            form.save()
            return redirect('list_department')
    else:
        form = departmentForm(instance = department_data)
    context = {'form':form,'dep_id':dep_id}
    return render(request,'userEmployee/update/department.html',context)
def delete_department(request,dep_id):
    department_data = get_object_or_404(department, dep_id=dep_id)
    department_data.delete()
    return redirect('list_department')

def list_tool(requset):
    data = tool.objects.all().order_by('tool_id')
    context = {'data':data}
    return render(requset, 'userEmployee/list/tool.html', context)
def add_tool(request) :
    form = toolForm()
    if request.method == "POST":
        form = toolForm(data=request.POST,files=request.FILES or None)
        if form.is_valid():
            get_form = form.save(commit=False)
            id = tool.objects.values_list('tool_id', flat=True).last()
            if id is None:
                tool_id = 'tool_00001'
            else:
                str_id = str(id)
                position_id_number = str_id.rfind("_") + 1
                str_id = str_id[position_id_number:10]
                number_id = int(str_id) + 1
                number_len = len(str_id) - len(str(number_id))
                id_first = 'tool_'
                for number_1 in range(0, number_len):
                    id_first = id_first + '0'
                tool_id = id_first + str(number_id)

            filepath = get_form.tool_img.name
            if filepath is not None:
                filepath = get_form.tool_img.name
                position_number = filepath.rfind('.')
                ext = filepath[position_number:]

                filepath_name = filepath.split('/')
                old_name = filepath_name[len(filepath_name) - 1]
                new_name = tool_id + ext
                get_form.tool_id = tool_id
                get_form.save()

                tools = get_object_or_404(tool, tool_id=tool_id)
                tools.tool_img.name = '/images/tool/' + new_name
                tools.save()

                if os.path.exists('static/images/tool/' + new_name):
                    os.remove('static/images/tool/' + new_name)
                os.rename('static/images/tool/' + old_name, 'static/images/tool/' + new_name)
            else:
                get_form.tool_id = tool_id
                get_form.save()
            return redirect('list_tool')
    context = {'form':form}
    return render(request,'userEmployee/insert/tool.html',context)
def update_tool(request,tool_id) :
    tool_data = get_object_or_404(tool, tool_id=tool_id)
    tool_img = tool_data.tool_img.name
    form = toolForm(instance=tool_data)
    if request.method == 'POST':
        form = toolForm(data=request.POST or None, files=request.FILES or None, instance=tool_data)
        if form.is_valid():
            get_form = form.save(commit=False)
            if get_form.tool_img.name != tool_img:
                tool_id = get_form.tool_id
                filepath = get_form.tool_img.name
                position_number = filepath.rfind('.')
                ext = filepath[position_number:]

                filepath_name = filepath.split('/')
                old_name = filepath_name[len(filepath_name) - 1]
                new_name = tool_id + ext
                get_form.save()

                tools = get_object_or_404(tool, tool_id=tool_id)
                tools.tool_img.name = '/images/tool/' + new_name
                tools.save()

                if os.path.exists('static/images/tool/' + new_name):
                    os.remove('static/images/tool/' + new_name)
                os.rename('static/images/tool/' + old_name, 'static/images/tool/' + new_name)
                return redirect('update_tool', tool_id=tool_id)
            else:
                get_form.save()
                return redirect('update_tool', tool_id=tool_id)
        else:
            form = toolForm(instance=tool_data)
    context = {'form': form, 'tool_img': tool_img, 'tool_id': tool_id}
    return render(request,'userEmployee/update/tool.html',context)
def delete_tool(request,tool_id) :
    tool_data = get_object_or_404(tool, tool_id=tool_id)
    if tool_data.tool_img == '':
        tool_data.delete()
    else:
        os.remove('static/' + tool_data.tool_img.name)
        tool_data.delete()
    return redirect('list_tool')
def list_tooltype(request):
    tooltype_data = tooltype.objects.all().order_by("tooly_id")
    context = {'context':tooltype_data}
    return  render(request, 'userEmployee/list/tooltype.html', context)
def add_tooltype(request):
    if request.method == 'POST':
        form = tooltypeForm(data=request.POST)
        if form.is_valid():
            get_form = form.save(commit=False)
            id = tooltype.objects.values_list('tooly_id', flat=True).last()
            if id is None:
                tooly_id = 'tooly_0001'
            else:
                str_id = str(id)
                position_id_number = str_id.rfind("_")+1
                str_id = str_id[position_id_number:10]
                number_id = int(str_id) + 1
                number_len = len(str_id) - len(str(number_id))
                id_first = 'tooly_'
                for number_1 in range(0,number_len):
                    id_first = id_first + '0'
                tooly_id = id_first+str(number_id)
            # จบเพิ่มที่ละเลข
            get_form.tooly_id = tooly_id
            get_form.save()
            return redirect('list_tooltype')

    else:
        form = tooltypeForm()
    context = {'form':form}
    return render(request,'userEmployee/insert/tooltype.html',context)
def update_tooltype(request,tooly_id):
    tooltype_data = get_object_or_404(tooltype, tooly_id=tooly_id)
    if request.method == 'POST':
        form = tooltypeForm(data=request.POST,instance=tooltype_data)
        if form.is_valid():
            form.save()
            return redirect('list_tooltype')
    else:
        form = tooltypeForm(instance = tooltype_data)
    context = {'form':form,'tooly_id':tooly_id}
    return render(request,'userEmployee/update/tooltype.html',context)
def delete_tooltype(request,tooly_id):
    tooltype_data = get_object_or_404(tooltype, tooly_id=tooly_id)
    tooltype_data.delete()
    return redirect('list_tooltype')