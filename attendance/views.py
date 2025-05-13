from .models import *
from .forms import *
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, datetime, timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import csv


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


#@login_required
def dashboard(request):
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    total_shifts = Shift.objects.count()
    total_holidays = Holiday.objects.count()
    attendance_today = Attendance.objects.filter(date=date.today()).count()
    holidays = Holiday.objects.filter(date__gte=date.today()).order_by('date')[:8]
    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_shifts': total_shifts,
        'total_holidays': total_holidays,
        'holidays': holidays,
        'attendance_today': attendance_today

    }
    return render(request, 'dashboard.html', context)


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})


def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee created successfully!")
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form, 'action': 'Create'})


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully!")
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form, 'action': 'Update'})


# Delete an employee (Delete)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})


# Department List View
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})


def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')  # Redirect to department list or another view
    else:
        form = DepartmentForm()

    return render(request, 'department_form.html', {'form': form})


# Shift List View
def shift_list(request):
    shifts = Shift.objects.all()
    return render(request, 'shift_list.html', {'shifts': shifts})


def create_shift(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shift_list')  # Redirect to department list or another view
    else:
        form = ShiftForm()

    return render(request, 'shift_form.html', {'form': form})


def shift_update(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully!")
            return redirect('shift_list')
    else:
        form = ShiftForm(instance=shift)
    return render(request, 'shift_form.html', {'form': form, 'action': 'Update'})


# Delete an employee (Delete)
def shift_delete(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    if request.method == 'POST':
        shift.delete()
        messages.success(request, "Shift deleted successfully!")
        return redirect('shift_list')
    return render(request, 'shift_confirm_delete.html', {'shift': shift})


# Assign Shift to Employee
def assign_shift(request):
    if request.method == 'POST':
        form = ShiftAssignmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Shift assigned successfully!")
                return redirect('assigned_shift_list')  # Assigned shift list এ রিডাইরেক্ট করুন
            except IntegrityError:
                messages.error(request, "This employee already has a shift assigned for this date.")
        else:
            messages.error(request, "Invalid data. Please check the inputs.")
    else:
        form = ShiftAssignmentForm()
    return render(request, 'assign_shift.html', {'form': form})


def assigned_shift_list(request):
    assigned_shifts = ShiftAssignment.objects.select_related('employee', 'shift').order_by('-date')
    return render(request, 'assigned_shift_list.html', {'assigned_shifts': assigned_shifts})


#@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')[:50]
    return render(request, 'attendance_list.html', {'attendances': attendances})


#@login_required
def upload_attendance(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                emp_id = row.get('ID')
                date_str = row.get('Date')
                check_in = row.get('CheckIn')
                check_out = row.get('CheckOut')

                try:
                    employee = Employee.objects.get(employee_id=emp_id)
                except Employee.DoesNotExist:
                    messages.warning(request, f"Employee ID {emp_id} not found in the system.")
                    continue

                try:
                    date_obj = datetime.strptime(date_str, '%m/%d/%Y').date()
                    check_in_time = datetime.strptime(check_in, '%H:%M').time()
                    check_out_time = datetime.strptime(check_out, '%H:%M').time()

                    check_in_datetime = datetime.combine(date_obj, check_in_time)
                    check_out_datetime = datetime.combine(date_obj, check_out_time)

                    working_seconds = (check_out_datetime - check_in_datetime).total_seconds()
                    working_hours = working_seconds / 3600  # seconds to hours

                    standard_hours = 8
                    overtime_hours = working_hours - standard_hours if working_hours > standard_hours else 0

                    Attendance.objects.update_or_create(
                        employee=employee,
                        date=date_obj,
                        defaults={
                            'check_in': check_in_time,
                            'check_out': check_out_time,
                            'status': 'Present',
                            'working_hours': round(working_hours, 2),
                            'overtime_hours': round(overtime_hours, 2),
                        }
                    )
                except Exception as e:
                    messages.warning(request, f"Error processing row: {row} — {str(e)}")

            messages.success(request, 'CSV uploaded and attendance updated!')
            return redirect('attendance_list')
    else:
        form = CSVUploadForm()

    return render(request, 'upload_attendance.html', {'form': form})


def holiday_list(request):
    holidays = Holiday.objects.all().order_by('date')
    return render(request, 'holiday_list.html', {'holidays': holidays})


def add_holiday(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        Holiday.objects.create(name=name, date=date)
        messages.success(request, "Holiday added successfully!")
        return redirect('holiday_list')
    return render(request, 'add_holiday.html')


def holiday_delete(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        holiday.delete()
        messages.success(request, "Holiday deleted successfully!")
        return redirect('holiday_list')
    return render(request, 'holiday_confirm_delete.html', {'holiday': holiday})


def monthly_work_summary(request):
    attendances = Attendance.objects.filter(status='Present')

    summary = attendances.annotate(
        month=TruncMonth('date')
    ).values(
        'employee__employee_id',
        'employee__user__username',  # Fixed this
        'month'
    ).annotate(
        total_working_hours=Sum('working_hours'),
        total_overtime_hours=Sum('overtime_hours')
    ).order_by('employee__employee_id', 'month')

    return render(request, 'monthly_work_summary.html', {'summary': summary})


def export_monthly_summary_csv(request):

    attendances = Attendance.objects.filter(status='Present')

    summary = attendances.annotate(
        month=TruncMonth('date')
    ).values(
        'employee__employee_id', 'employee__user__username', 'month'
    ).annotate(
        total_working_hours=Sum('working_hours'),
        total_overtime_hours=Sum('overtime_hours')
    ).order_by('employee__employee_id', 'month')

    # CSV Response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="monthly_summary.csv"'

    writer = csv.writer(response)

    # Write header
    writer.writerow(['Employee ID', 'Employee Name', 'Month', 'Total Working Hours', 'Total Overtime Hours'])

    # Write data rows
    for record in summary:
        writer.writerow([
            record['employee__employee_id'],
            record['employee__user__username'],
            record['month'].strftime('%B %Y'),  # Example: April 2025
            round(record['total_working_hours'], 2) if record['total_working_hours'] else 0,
            round(record['total_overtime_hours'], 2) if record['total_overtime_hours'] else 0
        ])

    return response