from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

class Employee(models.Model):
    SHIFT_CHOICES = [
        ('day', 'Day Shift (9:30 AM - 6:00 PM)'),
        ('night', 'Night Shift (11:00 PM - 7:30 AM)'),
    ]

    name = models.CharField(max_length=100)
    UserNaMe = models.CharField(max_length=100, null=True, blank=True, default="")
    PassWoRd = models.CharField(max_length=100, null=True, blank=True, default="")
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True,blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    location=models.CharField(max_length=100,null=True,blank=True)
    position = models.CharField(max_length=100)
    date_joined = models.DateField()
    salary = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, default="day")
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)
    rotation_date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('on_leave', 'On Leave'),
    ]

    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return f'{self.employee.name} - {self.date} - {self.status}'

class JobVacancy(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    qualifications = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Process(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="processes", default=1)
    assigned_to = models.ManyToManyField(Employee, related_name='assigned_processes')
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')],
        default='pending'
    )

    def __str__(self):
        return self.name

