from django.conf.urls import include, url

import leavemanagement
from leavemanagement.views import EmployeeView, timeoffapply
from . import views

urlpatterns = {
    url(r'^$', EmployeeView.as_view()),
    url(r'^apply',timeoffapply),
}