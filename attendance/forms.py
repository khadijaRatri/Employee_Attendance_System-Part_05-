from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select CSV file')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Employee Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


# Department Form
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


# Shift Form
class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'


# Shift Assignment Form
class ShiftAssignmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ShiftAssignment
        fields = ['employee', 'shift', 'date']


# Holiday Form
class HolidayForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Holiday
        fields = ['name', 'date']