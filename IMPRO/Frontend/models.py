from django.db import models
from Backend.models import JobVacancy
from django.contrib.auth.models import User

# Create your models here.
    

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Interview Scheduled', 'Interview Scheduled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    current_position = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=20)
    education = models.CharField(max_length=50)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/')
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-applied_date']