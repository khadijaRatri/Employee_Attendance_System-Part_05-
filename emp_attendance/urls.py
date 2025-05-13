"""
URL configuration for employee_attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from attendance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('upload/', views.upload_attendance, name='upload_attendance'),
    path('monthly_summary/', views.monthly_work_summary, name='monthly_summary'),
    path('export_monthly_summary_csv/', views.export_monthly_summary_csv, name='export_monthly_summary_csv'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/update/<int:pk>/', views.employee_update, name='employee_update'),
    path('employees/delete/<int:pk>/', views.employee_delete, name='employee_delete'),

    path('departments/', views.department_list, name='department_list'),
    path('department/create/', views.create_department, name='create_department'),

    path('shifts/', views.shift_list, name='shift_list'),
    path('shifts/create/', views.create_shift, name='create_shift'),
    path('shifts/update/<int:pk>/', views.shift_update, name='shift_update'),
    path('shifts/delete/<int:pk>/', views.shift_delete, name='shift_delete'),

    path('assign-shift/', views.assign_shift, name='assign_shift'),
    path('assigned-shifts/', views.assigned_shift_list, name='assigned_shift_list'),


    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.add_holiday, name='add_holiday'),
    path('holidays/delete/<int:pk>/', views.holiday_delete, name='holiday_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
