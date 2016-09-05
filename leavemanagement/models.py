from django.db import models


# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    dob = models.DateField()
    joining_date = models.DateField()
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Employee_Relation(models.Model):
    Employee_id = models.IntegerField()
    Manager_id = models.IntegerField()


class Leave_type(models.Model):
    type = models.CharField(max_length=200)
    max_days = models.IntegerField()

class Leave(models.Model):
    Employee_id = models.IntegerField()
    leave_type_id = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=200)






