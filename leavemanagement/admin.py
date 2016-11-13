from django.contrib import admin

# Register your models here.
from .models import Employee, Leave_type


class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['email']}),
        (None, {'fields': ['password']}),
        (None, {'fields': ['dob']}),
        (None, {'fields': ['joining_date']}),
        (None, {'fields': ['role']}),

    ]


class Leave_typeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['type']}),
        (None, {'fields': ['max_days']})
    ]


admin.site.register(Leave_type,Leave_typeAdmin)
admin.site.register(Employee,EmployeeAdmin)

