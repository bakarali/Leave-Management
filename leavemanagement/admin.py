from django.contrib import admin

# Register your models here.
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['email']}),
        (None, {'fields': ['password']}),
        (None, {'fields': ['dob']}),
        (None, {'fields': ['joining_date']}),
        (None, {'fields': ['role']}),

    ]

admin.site.register(Employee,EmployeeAdmin)

