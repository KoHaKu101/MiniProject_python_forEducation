import os


from django.shortcuts import render,redirect,get_object_or_404
from datetime import datetime

from .form import *
from Python_Project.defaultfunction.function import *
from Project_UserEmp.models import order_payment
from Project_UserEmp.models import order as order_cus
def homepage(request):
    order_data_success = order_cus.objects.filter(order_status=4).all().order_by('order_id')[:10]
    order_data_news = order_cus.objects.filter(order_status=0).all().order_by('order_id')[:10]
    context = {'order_data_success':order_data_success,'order_data_news':order_data_news}
    return render(request,'cus/home.html',context)
def register(request):
    form = customerForm()
    if request.method == "POST":
        form = customerForm(data=request.POST)
        email = request.POST['email']
        data_customer = customer.objects.filter(email=email)
        if data_customer.count() > 0:
            icon = 'error'
            text = 'อีเมลล์นี้ถูกใช้งานแล้ว'
            status = '0'
            context = {'form': form, 'status': status, 'text': text, 'icon': icon}
            return render(request, 'cus/register.html', context)
        if form.is_valid():
            get_form = form.save(commit=False)
            id = customer.objects.values_list('cus_id', flat=True).last()
            cus_id = id_generate("cus",id)
            get_form.cus_id = cus_id
            get_form.save()
            return redirect('cus_home')
        else:
            form = customerForm(data=request.POST)
    context = {'form':form}
    return render(request, 'cus/register.html',context)
def repair_form(request):
    if request.session.get('is_login'):
        form = orderForm()
        if request.method == "POST":
            form = orderForm(data=request.POST,files=request.FILES or None)
            if form.is_valid():
                get_form = form.save(commit=False)
                id = order.objects.values_list('order_id', flat=True).last()
                if id is None:
                    order_id = 'order_0001'
                else:
                    str_id = str(id)
                    position_id_number = str_id.rfind("_") + 1
                    str_id = str_id[position_id_number:10]
                    number_id = int(str_id) + 1
                    number_len = len(str_id) - len(str(number_id))
                    id_first = 'order_'
                    for number_1 in range(0, number_len):
                        id_first = id_first + '0'
                    order_id = id_first + str(number_id)

                filepath = get_form.order_img.name
                position_number = filepath.rfind('.')
                ext = filepath[position_number:]
                filepath_name = filepath.split('/')
                old_name = filepath_name[len(filepath_name) - 1]
                new_name = order_id + ext
                get_form.order_id = order_id
                get_form.create_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                get_form.cus_id = request.session.get('id')
                get_form.save()
                orders = get_object_or_404(order, order_id=order_id)
                orders.order_img.name = '/images/orders/' + new_name
                orders.save()

                if os.path.exists('static/images/orders/' + new_name):
                    os.remove('static/images/orders/' + new_name)
                os.rename('static/images/orders/' + old_name, 'static/images/orders/' + new_name)

                return redirect('cus_repair_list')
            else:
                form = orderForm(data=request.POST)
        context = {'form': form}
        return render(request,'cus/repairForm.html',context)
    else:
        return redirect('cus_login')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        data_customer = customer.objects.filter(email = email).values('cus_id','first_name','email','password')
        if data_customer.count() > 0 :
            customer_id = data_customer[0]['cus_id']
            customer_email = data_customer[0]['email']
            customer_password = data_customer[0]['password']
            if password == customer_password and email == customer_email:
                request.session["username"] = data_customer[0]['first_name']
                request.session["id"] = customer_id
                request.session["is_login"] = True
                request.session["status"] = "cus"
                return redirect('cus_home')
            else:
                icon = 'error'
                text = 'รหัสผ่านผิด'
                status = '0'

        else:
            icon = 'error'
            text = 'ไม่พบผู้ใช้นี้'
            status = '0'
        context = {'status': status, 'text': text, 'icon': icon}
        return render(request, 'cus/login.html',context)
    return render(request,'cus/login.html')
def logout(request):
    del request.session["username"]
    del request.session["id"]
    del request.session["is_login"]
    del request.session["status"]
    return redirect('cus_home')

def repair_list(request):
    if request.session.get('is_login'):
        order_rec_data = order_receive.objects.filter(order__cus_id=request.session.get('id')).values_list('price',flat=True).order_by('order_id')
        order_data = order.objects.filter(cus_id = request.session.get('id')).all().order_by('order_id')
        order_data = page_paganition(request,order_data,5)
        context = {'order_rec_data':order_rec_data,'order_data':order_data}
        return render(request,'cus/repairList.html',context)
    else:
        return redirect('cus_login')
def check_out(request,order_id):
    cus_id = request.session.get('id')
    order_rec = get_object_or_404(order_receive, order_id=order_id)
    cus_add = cus_address.objects.filter(cus_id=cus_id).all()
    order_rec_id = order_rec.order_rec_id
    order_data = get_object_or_404(order_cus, order_id=order_id)
    if order_data.order_status == 3:
        return redirect('check_out_qrcode',order_rec_id)
    if request.method == "POST":
        if cus_add.count() > 0:
            cus_add = get_object_or_404(cus_address, cus_id=cus_id)
            form = addresssForm(data=request.POST,instance=cus_add)
        else:
            form = addresssForm(data=request.POST)
        if form.is_valid():
            cus_add = cus_address.objects.filter(cus_id = cus_id).all()
            payment = order_payment.objects.values_list('pay_id',flat=True).last()
            order = order_cus.objects.filter(order_id = order_id).all()
            pay_type = request.POST["pay_type"]
            if cus_add.count() > 0:
                form = form.save(commit=False)
                form.save()
            else:
                cus_add = cus_address.objects.values_list('cus_add', flat=True).last()
                form_add = form.save(commit=False)
                form_add.cus_add = id_generate("add",cus_add)
                form_add.cus_id = cus_id
                form_add.save()
            form_pay = payForm()
            form_pay = form_pay.save(commit=False)
            form_pay.pay_id = id_generate("pay",payment)
            form_pay.order_rec_id = order_rec_id
            form_pay.pay_type = pay_type
            form_pay.pay_status = '1'
            form_pay.save()
            order.update(order_status = 3)
            if pay_type == "1":
                return redirect("check_out_success",order_rec_id)
            else:
                return redirect("check_out_qrcode",order_rec_id)
    cus_data = get_object_or_404(customer,cus_id = cus_id)
    tool_use_data = tool_use.objects.filter(order_receive_id = order_rec_id).all()
    if cus_add.count() > 0:
        cus_add = get_object_or_404(cus_address, cus_id=cus_id)
        form = addresssForm(instance=cus_add)
    else:
        form = addresssForm()
    context = {'tool_use_data':tool_use_data,'order_rec':order_rec,'cus_data':cus_data,'form':form}
    return render(request, 'cus/checkout.html', context)

def check_out_qrcode(request,order_rec_id):
    payment = get_object_or_404(order_payment,order_rec_id = order_rec_id)
    if payment.pay_type == 1 or payment.pay_status == '2':
        return redirect('check_out_success',order_rec_id)
    if request.method == "POST":
        form = payForm(data=request.POST,files=request.FILES,instance=payment)
        if form.is_valid():
            form = form.save(commit=False)
            form.pay_status = "2"
            form.pay_date_send = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            id = form.pay_id

            filepath = form.pay_img.name
            position_number = filepath.rfind('.')
            print(position_number)
            ext = filepath[position_number:]
            filepath_name = filepath.split('/')
            old_name = filepath_name[len(filepath_name) - 1]
            new_name = id + ext
            form.save()

            payment = get_object_or_404(order_payment,pay_id = id)
            payment.pay_img.name = '/images/pay/' + new_name
            payment.save()

            if os.path.exists('static/images/pay/' + new_name):
                os.remove('static/images/pay/' + new_name)
            os.rename('static/images/pay/' + old_name, 'static/images/pay/' + new_name)
            return redirect('check_out_success',order_rec_id)
    form = payForm()
    context = {'form': form,'order_rec_id':order_rec_id}
    return render(request,'cus/qrcode_page.html',context)

def check_out_success(request,order_rec_id):
    order_rec = get_object_or_404(order_receive,order_rec_id = order_rec_id)
    context = {'order_rec':order_rec}
    return render(request,'cus/checkout_success.html',context)