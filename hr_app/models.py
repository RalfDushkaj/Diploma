from django.db import models
from datetime import date

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female','Female'), ('Other','Other')])
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=50)
    hire_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    full_time = models.BooleanField(default=True)

    WORK_TYPE_CHOICES = [
        ('Remote', 'Remote'),
        ('Onsite', 'Onsite'),
    ] 
    work_type = models.CharField(max_length=10, choices=WORK_TYPE_CHOICES, blank=True, null=True)

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('On Leave', 'On Leave'),
    ]
    work_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name    
    

