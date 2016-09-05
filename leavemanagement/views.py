# Create your views here.
from django.forms import forms
from django.shortcuts import render
from django.template.context_processors import request
from django.utils import timezone
from django.views import generic


from leavemanagement.models import Employee, Leave


class EmployeeView(generic.ListView):
      model = Employee
      template_name = "timeoff.html"
      context_object_name = "apply_leave"

      def get_queryset(self):
          """Return the last five published questions."""
          return Employee.objects.order_by('-id')

def timeoffapply(request):
    stdate = request.POST['startDate']
    enddate = request.POST['endDate']
    leavetype = request.POST['leaveType']
    test = Leave(id=6,Employee_id=1,leave_type_id=1,start_date=stdate,end_date=enddate,status="pending")
    test.save()
    return render(request, 'timeoff.html', {
        'message': "You didn't select a choice.",
    })

