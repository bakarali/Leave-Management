from django.contrib import admin

# Register your models here.
from .models import Employee, Leave_type, Employee_Relation


class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['email']}),
        (None, {'fields': ['password']}),
        (None, {'fields': ['dob']}),
        (None, {'fields': ['joining_date']}),
        (None, {'fields': ['role']}),

    ]


class Employee_RelationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['Employee_id']}),
        (None, {'fields': ['Manager_id']})
    ]


class Leave_typeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['type']}),
        (None, {'fields': ['max_days']})
    ]

admin.site.register(Employee_Relation, Employee_RelationAdmin)
admin.site.register(Leave_type, Leave_typeAdmin)
admin.site.register(Employee, EmployeeAdmin)
