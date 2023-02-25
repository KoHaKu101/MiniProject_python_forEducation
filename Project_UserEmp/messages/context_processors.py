from Project_UserEmp.models import employee


def my_session_processor(request):
    id = request.session.get('id', None)
    emp = request.session.get('status', None)
    if emp == 'emp':
        emp_data = employee.objects.filter(id = id).all()
        username = emp_data[0].first_name +" "+ emp_data[0].sur_name
        img = emp_data[0].img_profile
    else:
        username = ""
        img = ""
    return {'username': username,'img_profile_admin':img}