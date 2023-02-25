import os
from Python_Project.defaultfunction.function import *
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from Project_UserEmp.form import *
from Project_UserEmp.models import *
from Project_UserEmp.models import order as order_cus
from Project_Cus.models import cus_address
from django.db.models import Q,Sum
from datetime import datetime

def emp_login(request):
    if check_login_emp(request) is True:
        return redirect('emp_home')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        data_emp = employee.objects.filter(username = username).values('id','username','password','appointment')
        if data_emp.count() > 0 :
            data_emp = data_emp[0]
            emp_email = data_emp['username']
            emp_password = data_emp['password']
            if password == emp_password and username == emp_email:
                request.session["username"] = data_emp['username']
                request.session["id"] = data_emp['id']
                request.session["is_login"] = True
                request.session["status"] = "emp"
                return redirect('emp_home')
            else:
                icon = 'error'
                text = 'รหัสผ่านผิด'
                status = '0'
        else:
            icon = 'error'
            text = 'ไม่พบชื่อผู้ใช้นี้'
            status = '0'
        context = {'status':status,'text':text,'icon':icon}
        return render(request,'userEmployee/login.html',context)
    return render(request, 'userEmployee/login.html')
def emp_home(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    order_wait = order_cus.objects.filter(order_status=0).all().count()
    order_do = order_cus.objects.filter(order_status=1).all().count()
    order_check = order_cus.objects.filter(order_status__gt=1,order_status__lt=4).all().count()
    order_fail = order_cus.objects.filter(order_status=5).all().count()
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    repair_detail_data = []
    str_month = month[:1]
    for i in range(1,13) :
        if i > 9 :
            month = str(i)
        else:
            month = str_month + str(i)
        full_date = year +'-'+ month
        sum_total_price = order_receive.objects.filter(repair_detail__re_date_end__icontains=full_date).aggregate(Sum('price_total'))
        print()
        if sum_total_price['price_total__sum'] is None :
            price = 0
        else:
            price = sum_total_price['price_total__sum']
        repair_detail_data.append(price)

    context = {'order_wait':order_wait,'order_do':order_do,'order_check':order_check,'order_fail':order_fail,'repair_detail_data':repair_detail_data}
    return render(request, 'userEmployee/home.html',context)
def list_emp(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    data = employee.objects.all().order_by('id')
    search_text = ""
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        data = employee.objects.filter(
            Q(first_name__icontains = search_text) | Q(sur_name__icontains = search_text) |
            Q(id__icontains=search_text)
        ).all().order_by('id')
    data = page_paganition(request, data, 10)
    context = {'data': data,'search_text':search_text}
    return render(request, 'userEmployee/list/emp.html', context)
def add_emp(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    if request.method == "POST":
        form = empForm(data = request.POST, files=request.FILES or None)
        if form.is_valid():
            get_form = form.save(commit=False)
            get_form.password = request.POST.get('password')
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
            if filepath != "":
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
    if check_login_emp(request) is False:
        return redirect('emp_login')
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
                return redirect('list_emp')
            else:

                get_form.save()
                return redirect('list_emp')
        else:
            form = empForm(instance=employee_data)
    else:
        form = empForm(instance=employee_data)
    form.updateForm()
    context = {'form' : form,'img_profile' : img_profile,'id':id}
    return render(request,'userEmployee/update/emp.html',context)
def delete_emp(request,id):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    try:
        emp_data = get_object_or_404(employee, id=id)
        if emp_data.id is not None:
            if emp_data.img_profile == '':
                emp_data.delete()
            else:
                file_name = emp_data.img_profile.name
                if emp_data.delete():
                    os.remove('static/' + file_name)
            return JsonResponse({'success': True, 'message': 'ลบรายการสำเร็จ.'})

        else:
            return JsonResponse({'success': False, 'message': 'ไม่พบรายการ.'})
    except :
        return JsonResponse({'success': False, 'message': 'ไม่สามารถลบได้ เพราะมีการใช้งานอยู่.'})
def list_appointment(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    data = appointment.objects.all().order_by("app_permission")
    search_text = ""
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        data = appointment.objects.filter(
            Q(app_id__icontains=search_text) | Q(app_name__icontains=search_text) ).all().order_by(
            "app_id")
    data = page_paganition(request, data, 10)
    context = {'data': data, 'search_text': search_text}
    return  render(request, 'userEmployee/list/appointment.html', context)
def add_appointment(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    if request.method == 'POST':
        form = appointmentForm(data=request.POST)
        if form.is_valid():
            get_form = form.save(commit=False)
            # เพิ่มที่ละเลข
            id = appointment.objects.values_list('app_id', flat=True).last()
            if id is None:
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
    if check_login_emp(request) is False:
        return redirect('emp_login')
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
    if check_login_emp(request) is False:
        return redirect('emp_login')
    try:
        appointment_data = get_object_or_404(appointment, app_id=app_id)
        if appointment_data.app_id is not None:
            appointment_data.delete()
            return JsonResponse({'success': True, 'message': 'ลบรายการสำเร็จ.'})

        else:
            return JsonResponse({'success': False, 'message': 'ไม่พบรายการ.'})
    except :
        return JsonResponse({'success': False, 'message': 'ไม่สามารถลบได้ เพราะมีการใช้งานอยู่.'})
def list_department(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    data = department.objects.all().order_by("dep_id")
    search_text = ""
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        data = department.objects.filter(Q(dep_id__icontains=search_text)|Q(dep_name_th=search_text)|Q(dep_name_en=search_text)).all().order_by("dep_id")
    data = page_paganition(request, data, 10)
    context = {'data': data, 'search_text': search_text}
    return  render(request, 'userEmployee/list/department.html', context)
def add_department(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
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
    if check_login_emp(request) is False:
        return redirect('emp_login')
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
    if check_login_emp(request) is False:
        return redirect('emp_login')
    try:
        department_data = get_object_or_404(department, dep_id=dep_id)
        if department_data.dep_id is not None:
            department_data.delete()
            return JsonResponse({'success': True, 'message': 'ลบรายการสำเร็จ.'})

        else:
            return JsonResponse({'success': False, 'message': 'ไม่พบรายการ.'})
    except :
        return JsonResponse({'success': False, 'message': 'ไม่สามารถลบได้ เพราะมีการใช้งานอยู่.'})
def list_tool(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    data = tool.objects.all().order_by('tool_id')

    search_text = ""
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        data = tool.objects.filter(
            Q(tool_name__icontains = search_text) | Q(tool_id__icontains = search_text) |
            Q(tool_type__tooly_name__icontains=search_text)
        ).all().order_by('tool_id')
    data = page_paganition(request, data, 10)
    context = {'data': data,'search_text':search_text}
    return render(request, 'userEmployee/list/tool.html', context)
def add_tool(request) :
    if check_login_emp(request) is False:
        return redirect('emp_login')
    form = toolForm()
    if request.method == "POST":
        form = toolForm(data=request.POST,files=request.FILES or None)
        if form.is_valid():
            get_form = form.save(commit=False)
            id = tool.objects.values_list('tool_id', flat=True).last()
            tool_id = id_generate("tool",id)
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
            return redirect('list_tool')
    context = {'form':form}
    return render(request,'userEmployee/insert/tool.html',context)
def update_tool(request,tool_id) :
    if check_login_emp(request) is False:
        return redirect('emp_login')
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
                return redirect('list_tool')
            else:
                get_form.save()
                return redirect('list_tool')
        else:
            form = toolForm(instance=tool_data)
    context = {'form': form, 'tool_img': tool_img, 'tool_id': tool_id}
    return render(request,'userEmployee/update/tool.html',context)
def delete_tool(request,tool_id) :
    if check_login_emp(request) is False:
        return redirect('emp_login')
    try:
        tool_data = get_object_or_404(tool, tool_id=tool_id)
        if tool_data.tool_id is not None:
            if tool_data.tool_img == '':
                tool_data.delete()
            else:
                file_name = tool_data.tool_img.name
                if tool_data.delete():
                    os.remove('static/' + file_name)
            return JsonResponse({'success': True, 'message': 'ลบรายการสำเร็จ.'})

        else:
            return JsonResponse({'success': False, 'message': 'ไม่พบรายการ.'})
    except :
        return JsonResponse({'success': False, 'message': 'ไม่สามารถลบได้ เพราะมีการใช้งานอยู่.'})
def list_tooltype(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    data = tooltype.objects.all().order_by("tooly_id")
    search_text = ""
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        data = tooltype.objects.filter(
            Q(tooly_name__icontains=search_text) | Q(tooly_id__icontains=search_text)
        ).all().order_by('tooly_id')
    data = page_paganition(request, data, 10)
    context = {'data': data, 'search_text': search_text}
    return  render(request, 'userEmployee/list/tooltype.html', context)
def add_tooltype(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
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
    if check_login_emp(request) is False:
        return redirect('emp_login')
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
    if check_login_emp(request) is False:
        return redirect('emp_login')
    try:
        tooltype_data = get_object_or_404(tooltype, tooly_id=tooly_id)
        if tooltype_data.tooly_id is not None:
            tooltype_data.delete()
            return JsonResponse({'success': True, 'message': 'ลบรายการสำเร็จ.'})

        else:
            return JsonResponse({'success': False, 'message': 'ไม่พบรายการ.'})
    except :
        return JsonResponse({'success': False, 'message': 'ไม่สามารถลบได้ เพราะมีการใช้งานอยู่.'})
def list_order(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    data = order.objects.all().order_by("order_status")
    search_text = ""
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        data = order.objects.filter(order_id__icontains= search_text).all().order_by("order_status")
    data = page_paganition(request, data, 10)
    context = {'data':data,'search_text':search_text}
    return render(request,'userEmployee/list/order.html',context)
def view_order(request,order_id):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    order_data = get_object_or_404(order,order_id = order_id)
    tool_data = tool.objects.all().order_by('tool_id')
    context = {'order_data': order_data, 'tool_data': tool_data}
    if order_data.order_status == 1 or order_data.order_status == 5:
        form = repairDetailFrom()
        context = {'order_data': order_data, 'tool_data': tool_data,'form':form}
    elif order_data.order_status > 1:
        return redirect('check_emp_order',order_id)
    if request.method == "POST":
        order_rec_id = get_object_or_404(order_receive,order_id = order_id).order_rec_id
        repair_detail_data = repair_detail.objects.values_list('re_id', flat=True).last()
        repair_detail_form = repairDetailFrom(data=request.POST)
        repair_detail_form = repair_detail_form.save(commit=False)
        repair_detail_form.re_id = id_generate("re",repair_detail_data)
        repair_detail_form.order_receive_id = order_rec_id
        repair_detail_form.emp_id = request.session.get('id')

        tool_use_form = toolUseForm()
        tool_use_form = tool_use_form.save(commit=False)
        data = len(request.POST.getlist('tool_amount[]'))
        price = 0
        price_service = setting_default.objects.values_list('service_paid',flat=True).last()
        if price_service is None :
            price_service = 0.00
        for key in range(0,data):
            price += float(request.POST.getlist('tool_total[]')[key])
            tool_use_data = tool_use.objects.values_list('tu_id', flat=True).last()
            tool_use_form.tu_amount = request.POST.getlist('tool_amount[]')[key]
            tool_use_form.tu_total_price = request.POST.getlist('tool_total[]')[key]
            tool_use_form.tool_id = request.POST.getlist('tool_id[]')[key]
            tool_use_form.tu_id = id_generate("tu",tool_use_data)
            tool_use_form.order_receive_id = order_rec_id
            tool_use_form.tu_get_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tool_use_form.save()

        price_total = price_service + price
        repair_detail_form.save()
        order_receive_data = order_receive.objects.filter(order_id=order_id)
        order_receive_data.update(price = price,price_service = price_service,price_total = price_total)
        order_receive_data.update(order_rec_status = "2")
        order_queue_data = order_queue.objects.filter(order_receive_id=order_rec_id)
        order_queue_data.update(order_que_status = "2")
        order_data = order.objects.filter(order_id=order_id)
        order_data.update(order_status = "2")
        return redirect('check_emp_order', order_id)
    return render(request, 'userEmployee/view/order.html', context)
def check_order(request,order_id):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    order_data = get_object_or_404(order, order_id=order_id)
    order_rec_data = get_object_or_404(order_receive, order_id=order_id)
    order_rec_id = order_rec_data.order_rec_id
    tool_use_data = tool_use.objects.filter(order_receive_id = order_rec_id).all()
    tool_data = tool.objects.all()
    repair_detail_data = get_object_or_404(repair_detail, order_receive_id=order_rec_id)
    form_repair_detail = repairDetailFrom(instance=repair_detail_data)
    form_repair_detail.updateForm()
    total_price = order_rec_data.price + order_rec_data.price_service
    context = {'order_data':order_data,"form":form_repair_detail,"tool_use_data":tool_use_data,'tool_data':tool_data,"order_rec_data":order_rec_data,'total_price':total_price}
    return render(request,'userEmployee/view/checkorder.html',context)
def receive_order(request,order_id):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    order_data = order.objects.filter(order_id = order_id)
    emp_data = employee.objects.filter(id=request.session.get('id')).values('id')
    order_id = str(order_data.values('order_id')[0]["order_id"])
    emp_id = str(emp_data[0]["id"])
    # Order Rec Start
    order_rec_id = order_receive.objects.values_list('order_rec_id', flat=True).last()
    order_rec_id = id_generate("rec",order_rec_id)
    form_order_receive = orderReceiveForm()
    form_order_receive = form_order_receive.save(commit=False)
    form_order_receive.order_rec_id = order_rec_id
    form_order_receive.order_rec_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    form_order_receive.order_rec_status = 1
    form_order_receive.emp_id = emp_id
    form_order_receive.order_id = order_id
    form_order_receive.save()
    # Order Rec End
    # *********************************************************************
    # Order Que Start
    order_que_data = order_queue.objects.values_list('order_que_id','order_que_date',"order_que_number").last()
    order_que_date = datetime.now().strftime('%Y-%m-%d')
    order_rec_id = order_receive.objects.filter(order_rec_id=order_rec_id).values('order_rec_id')
    order_rec_id = order_rec_id[0]["order_rec_id"]
    order_que_id = id_generate("que", order_que_data[0])
    # Order Que Start Number and ID
    if order_que_data is not None :
        if order_que_data[1] == order_que_date :
            order_que_number = order_que_data[2] + 1
        else:
            order_que_number = 1
    else:
        order_que_number = 1
    # Order Que End Number and ID
    form_order_que = orderQueueForm()
    form_order_que = form_order_que.save(commit=False)
    form_order_que.order_que_id = order_que_id
    form_order_que.order_receive_id = order_rec_id
    form_order_que.order_que_number = order_que_number
    form_order_que.order_que_date = order_que_date
    print(form_order_que.order_receive_id)
    form_order_que.save()
    # Order Que End
    order_data.update(order_status = "1")
    return redirect('view_emp_order',order_id)
def cancel_order(request,order_id):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    order_data = order.objects.filter(order_id=order_id)
    order_data.update(order_status=5)
    return redirect('list_emp_order')
def pay_confirm_list(request):
    if check_login_emp(request) is False:
        return redirect('emp_login')
    data = order_payment.objects.all()
    data = page_paganition(request,data,10)

    search_text = ""
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        data = order_payment.objects.filter(
            Q(pay_id__icontains=search_text) | Q(order_rec__order__title__icontains=search_text)
        ).all().order_by('pay_id')
    context = {'data': data, 'search_text': search_text}
    return render(request,'userEmployee/list/pay_confirm_list.html',context)
def pay_detail(request,order_rec_id):
    payment_data = get_object_or_404(order_payment,order_rec_id = order_rec_id)
    context = {'payment_data':payment_data}
    return render(request,'userEmployee/view/pay_detail.html',context)
def pay_confirm(request,order_rec_id):
    order_rec_data = get_object_or_404(order_receive,order_rec_id=order_rec_id)
    payment_data = order_payment.objects.filter(order_rec_id=order_rec_id).all()
    payment_data.update(pay_status = "3",pay_date_check = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    order_data = order_cus.objects.filter(order_id = order_rec_data.order_id).all()
    order_rec_data.order_rec_status = "3"
    order_rec_data.save()
    order_data.update(order_status = 4)
    return redirect('list_payment')
def setting(request):
    setting = setting_default.objects.all().first()
    form = settingForm(instance=setting)
    if request.method == "POST":
        form = settingForm(data= request.POST,instance=setting)
        if form.is_valid():
            form = form.save()
        form = settingForm(instance=setting)
    context = {'form':form}
    return render(request,'userEmployee/setting.html',context)

from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def report(request,order_rec_id):
    pdfmetrics.registerFont(TTFont('THSarabunNew', 'thsarabunnew-webfont.ttf'))
    template = get_template('userEmployee/pay_slip.html')

    payment_data = order_payment.objects.filter(order_rec_id = order_rec_id).all()
    address_cus = cus_address.objects.filter(cus_id = payment_data[0].order_rec.order.cus_id).all()
    tool_use_data = tool_use.objects.filter(order_receive_id = order_rec_id).all()

    # วันที่
    pay_date_check_str = payment_data[0].pay_date_check
    pay_date_check_str = pay_date_check_str.split(" ")
    date_format = '%Y-%m-%d'
    pay_date_check_date = datetime.strptime(pay_date_check_str[0], date_format).date()

    context = {"payment_data": payment_data[0],'address_cus':address_cus[0],'pay_date_check_date':pay_date_check_date,'tool_use_data':tool_use_data}
    html = template.render(context)

    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)