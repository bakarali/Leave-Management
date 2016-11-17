# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime

from leavemanagement.models import Leave, Leave_type, Employee


def EmployeeView(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        qs = Leave.objects.all().filter(Emp_id=(request.session['id'])[0])
        context = {
            "qs": qs
        }
        return render(request, "timeoff.html", context)


def timeoffapply(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        stdate = request.POST['startDate']
        enddate = request.POST['endDate']
        d1 = datetime.strptime(stdate, "%Y-%m-%d")
        d2 = datetime.strptime(enddate, "%Y-%m-%d")
        d3 = abs((d2 - d1).days)
        leavetype = request.POST['leaveType']
        getleaveid = list(zip(Leave_type.objects.filter(type=leavetype).values_list('id', flat=True))[0])
        split_lt_id = ("".join(str(e) for e in getleaveid))
        empid = (request.session['id'])[0]
        leave_id = Leave.objects.all().count()
        test = Leave(id=(leave_id + 1), Emp_id=empid, leave_type_id=split_lt_id, start_date=stdate, end_date=enddate,
                     days=d3,
                     status="pending")
        test.save()
        return HttpResponseRedirect('/')


def leaveRequestdisplay():
    leaveqs = Leave.objects.all().exclude(status="canceled")
    context = {
        "leaveqs": leaveqs
    }
    return context


def timeoffrequested(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        return render(request, 'timeoffrequests.html', leaveRequestdisplay())


def approve(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        lid = request.POST['leaveid']
        test = Leave.objects.get(id=lid)
        test.status = "Approved"
        test.save()

        return render(request, 'timeoffrequests.html', leaveRequestdisplay())


def decline(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        lid = request.POST['leaveid']
        test = Leave.objects.get(id=lid)
        test.status = "declined"
        test.save()

        return render(request, 'timeoffrequests.html', leaveRequestdisplay())


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
