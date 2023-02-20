import os

from django.shortcuts import render,redirect,get_object_or_404
from datetime import datetime

from .form import *


def homepage(request):
    return render(request,'cus/home.html')
def register(request):
    form = customerForm()
    if request.method == "POST":
        form = customerForm(data=request.POST,files=request.FILES or None)
        if form.is_valid():
            get_form = form.save(commit=False)
            id = customer.objects.values_list('cus_id', flat=True).last()
            if id is None:
                cus_id = 'cus_000001'
            else:
                str_id = str(id)
                position_id_number = str_id.rfind("_") + 1
                str_id = str_id[position_id_number:10]
                number_id = int(str_id) + 1
                number_len = len(str_id) - len(str(number_id))
                id_first = 'emp_'
                for number_1 in range(0, number_len):
                    id_first = id_first + '0'
                cus_id = id_first + str(number_id)
            get_form.cus_id = cus_id
            get_form.save()
            return redirect('cus_home')
        else:
            form = customerForm(data=request.POST)
    context = {'form':form}
    return render(request, 'cus/register.html',context)
def repair_form(request):
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
            get_form.create_date_time = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')
            get_form.cus_id = 'cus_000001'
            get_form.save()
            orders = get_object_or_404(order, order_id=order_id)
            orders.order_img.name = '/images/orders/' + new_name
            orders.save()

            if os.path.exists('static/images/orders/' + new_name):
                os.remove('static/images/orders/' + new_name)
            os.rename('static/images/orders/' + old_name, 'static/images/orders/' + new_name)

            return redirect('cus_home')
        else:
            form = orderForm(data=request.POST)
    context = {'form': form}
    return render(request,'cus/repairForm.html',context)