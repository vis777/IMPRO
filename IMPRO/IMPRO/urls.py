"""
URL configuration for IMPRO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
import Frontend.urls
from Backend import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Frontend/', include(Frontend.urls)),
    path('adminpage/', views.AdminPageView.as_view(), name='adminpage'),
    path('admin_login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('admin_logout/', views.AdminLogoutView.as_view(), name='admin_logout'),
    path("",views.IndexPageView.as_view(), name="index"),

    path('department/add/', views.AddDepartmentView.as_view(), name='add_department'),
    path('department/manage/', views.DepartmentListView.as_view(), name='manage_department'),
    path('department/edit/<int:pk>/', views.DepartmentUpdateView.as_view(), name='edit_department'),
    path('department/delete/<int:pk>/', views.DepartmentDeleteView.as_view(), name='delete_department'),
    path('deparment/update/<int:pk>/', views.DepartmentUpdateView.as_view(), name='updatedepartment'),

    path('employee/add/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('employee/manage/', views.EmployeeListView.as_view(), name='manage_employee'),
    path('employee/edit/<int:pk>/', views.EmployeeUpdateView.as_view(), name='edit_employee'),
    path('job_rotations/add/<int:employee_id>/', views.JobRotationView.as_view(), name='add_job_rotation'),
    # path('job-rotations/delete/<int:pk>/', views.JobRotationDeleteView.as_view(), name='delete_job_rotation'),
    path('employee/delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='delete_employee'),

    path('mark_attendance/', views.MarkAttendanceView.as_view(), name='mark_attendance'),
    path("attendance_records/", views.AttendanceRecordView.as_view(), name="attendance_records"),

    path('post_job/', views.JobVacancyCreateView.as_view(), name='post_job'),
    path('jobs/', views.JobVacancyListView.as_view(), name='job_list'),
    path('delete_job/<int:pk>/', views.JobVacancyDeleteView.as_view(), name='delete_job'),
    path('job/applications/', views.JobUserListView.as_view(), name='job_user_list'),
    path('application/<int:pk>/update/', views.JobApplicationUpdateView.as_view(), name='update_application_status'),
    path('processes/', views.ProcessListView.as_view(), name='process_list'),
    path('processes/add/', views.ProcessCreateView.as_view(), name='add_process'),
    path('processes/delete/<int:pk>/', views.ProcessDeleteView.as_view(), name='delete_process'),
    # path('api/employees/', views.EmployeeView.as_view(), name='employee-list'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
