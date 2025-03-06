from Frontend import views
from django.urls import path
urlpatterns = [
    path('employee/', views.EmployeePageView.as_view(), name='employeepage'),
    path('login/', views.EmployeeLoginView.as_view(), name='employee_login'),
    path('logout/', views.EmployeeLogoutView.as_view(), name='employee_logout'),
    path('userlogin/', views.UserLoginView.as_view(), name='user_login'),
    path('register/', views.SaveRegistrationView.as_view(), name='savereg'),
    # path('user-login/', views.UserLoginProcessView.as_view(), name='user_login_process'),
    path('userlogout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('vacancies/', views.JobListView.as_view(), name='list_job'), 
    path('user/', views.UserPageView.as_view(), name='userpage'),
    path('apply/<int:job_id>/', views.JobApplicationView.as_view(), name='apply_job'),
    path('submit_application/<int:vacancy_id>/', views.SubmitApplicationView.as_view(), name='submit_application'),
    path('applied_jobs/', views.AppliedJobsListView.as_view(), name='applied_jobs'),
    path("delete_jobs/<int:pk>/", views.DeleteApplicationView.as_view(), name="delete_jobs"),     
]
