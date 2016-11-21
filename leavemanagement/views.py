# Create your views here.
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime

from leavemanagement.models import Leave, Leave_type, Employee, Employee_Relation


def EmployeeView(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        qs = Leave.objects.all().filter(Emp_id=(request.session['id'])[0])
        qs1 = Employee.objects.all()
        context = {
            "qs": qs,
            "qs1": qs1
        }
        return render(request, "timeoff.html", context)


def timeoffapply(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        stdate = request.POST['startDate']
        enddate = request.POST['endDate']
        leavetype = request.POST['leaveType']
        days = list(zip(Leave_type.objects.filter(type=leavetype).values_list('max_days', flat=True))[0])
        lt = list(zip(Leave_type.objects.filter(type=leavetype).values_list('type', flat=True))[0])
        d1 = datetime.strptime(stdate, "%Y-%m-%d")
        d2 = datetime.strptime(enddate, "%Y-%m-%d")
        d3 = abs((d2 - d1).days)
        if days[0] >= d3 or lt == leavetype[0]:
            getleaveid = list(zip(Leave_type.objects.filter(type=leavetype).values_list('id', flat=True))[0])
            split_lt_id = ("".join(str(e) for e in getleaveid))
            empid = (request.session['id'])[0]
            leave_id = Leave.objects.all().count()
            test = Leave(id=(leave_id + 1), start_date=stdate, end_date=enddate,
                         days=d3,
                         status="pending")
            test.Emp_id_id = empid
            test.leave_type_id_id = split_lt_id
            test.save()
            # from_mail = list(zip(Employee.objects.filter(id=(request.session['id'])[0]).values_list('email', flat=True))[0])
            # to = list(zip(Employee_Relation.objects.filter(Employee_id=empid).values_list('Manager_id', flat=True))[0])
            # to_mail = list(zip(Employee.objects.filter(id = to[0]).values_list('email',flat = True))[0])
            # to = settings.EMAIL_HOST_USER
            # to_email = [to, to_mail]
            # send_mail(
            #     'Apply for leave',
            #     'Here is the message.',
            #     'bakaralisunasra@gmail.com',
            #     ['sunasra@gmail.com'],
            #     fail_silently=False,
            # )

        return HttpResponse(leavetype)


# def leaveRequestdisplay():
#
#     return context


def timeoffrequested(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        empid = (request.session['id'])[0]
        get_emp_id = Employee_Relation.objects.filter(Manager_id= empid).values_list('Employee_id', flat=True)
        get_leave = Leave.objects.filter(Emp_id__in = get_emp_id).exclude(status="canceled")
        context = {
                  "leaveqs": get_leave
        }
        return render(request, 'timeoffrequests.html', context)


def approve(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        lid = request.POST['leaveid']
        test = Leave.objects.get(id=lid)
        test.status = "Approved"
        test.save()
        return HttpResponseRedirect('/timeoffrequests')
        #return render(request, 'timeoffrequests.html', leaveRequestdisplay())


def decline(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        lid = request.POST['leaveid']
        test = Leave.objects.get(id=lid)
        test.status = "Declined"
        test.save()
        return HttpResponseRedirect('/timeoffrequests')
        #return render(request, 'timeoffrequests.html', leaveRequestdisplay())


def cancelleave(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        lid = request.POST['leaveid']
        test = Leave.objects.get(id=lid)
        test.status = "canceled"
        test.save()
        return HttpResponseRedirect('/')


def login(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        return HttpResponseRedirect('/')


def logged(request):
    Email = request.POST['Email']
    pwd = request.POST['password']
    if Employee.objects.filter(email=Email, password=pwd):
        test1 = Employee.objects.filter(email=Email, password=pwd)
        if test1.count() == 1:
            data = list(zip(Employee.objects.filter(email=Email, password=pwd).values_list('id', flat=True))[0])
            request.session['id'] = data

            # return HttpResponse(data)
            return HttpResponseRedirect('/')
    return render(request, 'login.html')


def logout(request):
    del request.session['id']
    request.session.modified = True
    return HttpResponseRedirect('/login')
