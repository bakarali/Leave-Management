# Create your views here.
from django.shortcuts import render, redirect

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
        leavetype = request.POST['leaveType']
        getleaveid = list(zip(Leave_type.objects.filter(type=leavetype).values_list('id', flat=True))[0])
        split_lt_id = ("".join(str(e) for e in getleaveid))
        empid = (request.session['id'])[0]
        leave_id = Leave.objects.all().count()
        test = Leave(id=(leave_id + 1), Emp_id=empid, leave_type_id=split_lt_id, start_date=stdate, end_date=enddate,
                     status="pending")
        test.save()
        qs = Leave.objects.all().filter(Emp_id=(request.session['id'])[0])
        context = {
            "qs": qs
        }
        return render(request, 'timeoff.html', context)


def leaveRequestdisplay():
    leaveqs = Leave.objects.all().exclude(status="cancel")
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
        test.status = "Approve"
        test.save()

        return render(request, 'timeoffrequests.html', leaveRequestdisplay())


def decline(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        lid = request.POST['leaveid']
        test = Leave.objects.get(id=lid)
        test.status = "decline"
        test.save()

        return render(request, 'timeoffrequests.html', leaveRequestdisplay())


def cancelleave(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:

        lid = request.POST['leaveid']
        test = Leave.objects.get(id=lid)
        test.status = "cancel"
        test.save()

        context = {
            "qs":
                Leave.objects.all().filter(Emp_id=(request.session['id'])[0]),
        }
        return render(request, 'timeoff.html', context)


def login(request):
    if not request.session.get('id', None):
        return render(request, 'login.html')
    else:
        qs1 = Leave.objects.all().filter(Emp_id=(request.session['id'])[0])
        context = {
            "qs": qs1

        }

        return render(request, 'timeoff.html', context)



def logged(request):
    Email = request.POST['Email']
    pwd = request.POST['password']
    if Employee.objects.filter(email=Email, password=pwd):
        test1 = Employee.objects.filter(email=Email, password=pwd)
        if test1.count() == 1:
            data = list(zip(Employee.objects.filter(email=Email, password=pwd).values_list('id', flat=True))[0])
            request.session['id'] = data
            qs = Leave.objects.all().filter(Emp_id=(request.session['id'])[0]).order_by().reverse()
            context = {
                "qs": qs,
            }
            # return HttpResponse(data)
            return render(request, 'timeoff.html', context)
    return render(request, 'login.html')


def logout(request):
    del request.session['id']
    request.session.modified = True
    return render(request, 'login.html')