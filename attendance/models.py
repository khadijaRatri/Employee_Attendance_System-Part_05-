from django.db import models
from django.contrib.auth.models import User


# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Employee Model
class Employee(models.Model):
    employee_id = models.CharField(max_length=10, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    join_date = models.DateField()
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee_id} - {self.user.username}"


# Shift Model
class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"


# Shift Assignment Model
class ShiftAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()  # Specific date for the shift

    class Meta:
        unique_together = ('employee', 'date')  # Ensure one shift per employee per day

    def __str__(self):
        return f"{self.employee} - {self.shift} on {self.date}"


# Attendance Model
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True)
    working_hours = models.FloatField(null=True, blank=True)
    overtime_hours = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"


# Holiday Model
class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name


# Report Model
class Report(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    report_type = models.CharField(
        max_length=50,
        choices=[('Daily', 'Daily'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')],
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.employee:
            return f"{self.report_type} Report for {self.employee}"
        elif self.department:
            return f"{self.report_type} Report for {self.department.name}"
        else:
            return f"{self.report_type} Report - {self.generated_at}"
