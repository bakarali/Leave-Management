from django.conf.urls import include, url

import leavemanagement
from leavemanagement.views import timeoffapply, EmployeeView, cancelleave, timeoffrequested, approve, decline, login, logged, \
    logout,changepassword, passwordchange
from . import views

urlpatterns = [
    url(r'^$', EmployeeView),
    url(r'^cancel', cancelleave),
    url(r'^timeoffrequests', timeoffrequested),
    url(r'^login', login),
    url(r'^logged', logged),
    url(r'^approve', approve),
    url(r'^decline', decline),
    url(r'^apply', timeoffapply),
    url(r'^logout', logout),
    url(r'^changepassword', changepassword),
    url(r'^passwordchange', passwordchange),

]
