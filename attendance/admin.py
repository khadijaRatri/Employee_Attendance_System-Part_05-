from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register([Department, Employee, Shift, ShiftAssignment, Holiday, Attendance, Report])