# Create your views here.
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models import Sum

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
        d3 = abs((d2 - d1).days)+1
        empid = (request.session['id'])[0]
        countdays = Leave.objects.filter(Emp_id = empid,type=leavetype).aggregate(Sum('days'))
        if countdays['days__sum'] == None:
            finaday = (days[0] - 0)
        else:
            finaday=(days[0] - countdays['days__sum'])
        if enddate>=stdate:
            if finaday >= d3:
                getleaveid = list(zip(Leave_type.objects.filter(type=leavetype).values_list('id', flat=True))[0])
                split_lt_id = ("".join(str(e) for e in getleaveid))
                empid = (request.session['id'])[0]
                get_emp_name = list(zip(Employee.objects.filter(id=empid).values_list('name', flat=True))[0])
                get_emp_name = ("".join(str(e) for e in get_emp_name))
                empid = (request.session['id'])[0]
                leave_id = Leave.objects.all().count()
                test = Leave(id=(leave_id + 1), name=get_emp_name, type=leavetype, start_date=stdate, end_date=enddate,
                             days=d3,
                             status="pending")

                test.Emp_id_id = empid
                test.leave_type_id_id = split_lt_id
                test.save()
                return HttpResponseRedirect('/')
            else:
                qs = Leave.objects.all().filter(Emp_id=(request.session['id'])[0])
                context = {
                    "qs": qs,
                    "error": "true",
                    "msg": "You are allowed to have holidays for " + str(finaday) + " days in " +str(leavetype)
                }
                return render(request, 'timeoff.html', context)


        else:
            qs = Leave.objects.all().filter(Emp_id=(request.session['id'])[0])
            context = {
                "qs":qs,
                "error": "true",
                "msg": "Start date should not be greater then End date"
            }
            return render(request, 'timeoff.html', context)


def timeoffrequested(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        empid = (request.session['id'])[0]
        get_emp_id = Employee_Relation.objects.filter(Manager_id=empid).values_list('Employee_id', flat=True)
        get_leave = Leave.objects.filter(Emp_id__in=get_emp_id).exclude(status="canceled")
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
        # return render(request, 'timeoffrequests.html', leaveRequestdisplay())


def decline(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        lid = request.POST['leaveid']
        test = Leave.objects.get(id=lid)
        test.status = "Declined"
        test.save()
        return HttpResponseRedirect('/timeoffrequests')
        # return render(request, 'timeoffrequests.html', leaveRequestdisplay())


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
    else:
        context = {
            "error": "true",
            "msg": "Login failed : Wrong credentials. Try again."

        }
        return render(request, 'login.html',context)



def logout(request):
    del request.session['id']
    request.session.modified = True
    return HttpResponseRedirect('/login')


def changepassword(request):

   return render(request, 'changepassword.html')


def passwordchange(request):
    oldpwd = request.POST['oldpwd']
    newpwd = request.POST['newpwd']
    cnfpwd = request.POST['cnfpwd']
    if oldpwd != newpwd:
        if Employee.objects.filter(password=oldpwd, id=(request.session['id'])[0]):
            if newpwd == cnfpwd:
                test = Employee.objects.get(id=(request.session['id'])[0])
                test.password = newpwd
                test.save()
                context = {
                    "status": "success",
                    "msg": "Password successfully changed!!"

                }
                return render(request, 'changepassword.html',context)
            else:
                context = {
                    "status": "error",
                    "msg": "Password does not match. Try again"

                }
                return render(request, 'changepassword.html',context)
        else:
            context = {
                "status": "error",
                "msg": "Old password is wrong. Try again"

            }
            return render(request, 'changepassword.html', context)
    else:
        context = {
            "status": "error",
            "msg": "Old password and New password should be different . Try again"

        }
        return render(request, 'changepassword.html', context)