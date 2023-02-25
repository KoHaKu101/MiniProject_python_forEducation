from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.shortcuts import render

def id_generate(firstname,id):
    if id is None:
        title = firstname+"_"
        number_str = len(title)
        max_number = 9 - number_str
        id = title
        for i in range(0,max_number):
            id = id + "0"
        id = id+"1"
    else:
        id = str(id)
        position_id_number = id.rfind("_") + 1
        str_id = id[position_id_number:10]
        number_id = int(str_id) + 1
        number_len = len(str_id) - len(str(number_id))
        title = firstname+"_"
        for i in range(0, number_len):
            title = title + '0'
        id = title + str(number_id)

    return id

def check_login_emp (request) -> bool:
    if request.session.get('is_login') and request.session.get('status') == "emp":
        return True
    else:
        return False

def page_paganition(request,data,items_per_page):
    paginator = Paginator(data, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page