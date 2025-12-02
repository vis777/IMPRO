from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from Frontend.models import JobApplication
from django.views.generic import FormView, View, CreateView, ListView, DetailView, TemplateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password, check_password
from Backend.models import Employee, Attendance, JobVacancy
from Frontend.forms import RegisterForm, JobApplicationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
class EmployeePageView(View):
    def get(self, request):
        # Get employee ID from session
        employee_id = request.session.get("employee_id")

        if not employee_id:
            messages.error(request, "Please log in first.")
            return redirect("employee_login")

        # Fetch the employee details
        employee = Employee.objects.get(id=employee_id)

        # Fetch attendance records for the logged-in employee
        attendance_records = Attendance.objects.filter(employee=employee).order_by("-date")

        # Fetch projects assigned to the logged-in employee
        assigned_projects = employee.assigned_processes.all()

        return render(request, "employeeindex.html", {
            "employee": employee,
            "attendance_records": attendance_records,
            "assigned_projects": assigned_projects,
        })

class EmployeeLoginView(View):
    template_name = "employeelogin.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        employee = Employee.objects.filter(UserNaMe=username, PassWoRd=password).first()

        if employee:
            if employee.status == "inactive":
                messages.error(request, "Your account is inactive. Contact admin.")
                return redirect("employee_login")  # Redirect back to login page

            # Store employee session
            request.session["employee_id"] = employee.id
            request.session["employee_name"] = employee.name

            # messages.success(request, "Login successful.")
            return redirect("employeepage")  # Redirect to employee dashboard

        else:
            messages.error(request, "Invalid username or password.")
            return redirect("employee_login")

class EmployeeLogoutView(View):
    def get(self, request):
        # messages.success(request, "Logout successful")
        return redirect('index')

class UserLoginView(View):
    """Handles rendering the login page."""
    template_name = "Logreg.html"
    success_url = reverse_lazy("userpage")

    def get(self, request):
        return render(request, "Logreg.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.success_url)
        else:
            messages.error(request, "Invalid username or password")
            return render(request, self.template_name)


class SaveRegistrationView(View):
    """Handles user registration using Django's built-in User model."""
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Secure password hashing
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('user_login')
        else:
            messages.error(request, "Registration failed. Please check the form.")
            return render(request, "Logreg.html", {"form": form})


# class UserLoginProcessView(View):
#     template_name = "Logreg.html"
#     success_url = reverse_lazy("userpage")

#     def post(self, request):
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect(self.success_url)
#         else:
#             messages.error(request, "Invalid username or password")
#             return render(request, self.template_name)


class UserLogoutView(View):
    """Handles user logout."""
    def get(self, request):
        logout(request)  # Properly log out user
        messages.success(request, "Logout successful")
        return redirect('index')


class UserPageView(LoginRequiredMixin, View):
    """Handles displaying the user dashboard with job listings."""
    template_name = "userindex.html"

    def get(self, request, *args, **kwargs):
        jobs = JobVacancy.objects.all().order_by('-posted_on')  # Fetch job vacancies
        return render(request, self.template_name, {'user': request.user, 'jobs': jobs})


class JobListView(ListView):
    model = JobVacancy
    template_name = 'Vacancy List.html'  # Specify the template
    context_object_name = 'vac'  # Define context name
    ordering = ['-posted_on']

class JobApplicationView(DetailView):
    model = JobVacancy
    template_name = 'Apply Job.html'
    context_object_name = 'vacancy'
    pk_url_kwarg = 'job_id'

    def handle_no_permission(self):
        messages.error(self.request, 'Job vacancy not found.')
        return redirect('list_job')

# class SubmitApplicationView(View):
#     def post(self, request, vacancy_id):
#         vacancy = get_object_or_404(JobVacancy, id=vacancy_id)
        
#         # application = JobApplication.objects.create(
#         #     vacancy=vacancy,
#         #     first_name=request.POST.get('first_name'),
#         #     last_name=request.POST.get('last_name'),
#         #     email=request.POST.get('email'),
#         #     phone=request.POST.get('phone'),
#         #     current_position=request.POST.get('current_position', ''),
#         #     experience=request.POST.get('experience'),
#         #     education=request.POST.get('education'),
#         #     cover_letter=request.POST.get('cover_letter', ''),
#         #     resume=request.FILES.get('resume'),
#         #     user=request.user
#         # )
#         application = JobApplicationForm(request.POST,request.FILES)
#         if application.is_valid():
#             data=form.save(commit=false,user=request.user)

#         return JsonResponse({"success": True})

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views import View
# from .models import JobApplication, JobVacancy
# from .forms import JobApplicationForm

# class SubmitApplicationView(View):
#     def post(self, request, vacancy_id):
#         vacancy = get_object_or_404(JobVacancy, id=vacancy_id)
        
#         # Bind form data
#         form = JobApplicationForm(request.POST, request.FILES)

#         if form.is_valid():
#             application = form.save(commit=False)  # Do not save yet
#             application.vacancy = vacancy  # Assign the vacancy
#             application.user = request.user
#             application.save()  # Save after assigning user
#             return JsonResponse({"success": True})
        
#         return JsonResponse({"success": False, "errors": form.errors})  # Send errors if invalid

class SubmitApplicationView(View):
    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(JobVacancy, id=vacancy_id)

        # 🔍 Debugging
        print("POST Data:", request.POST)
        print("FILES Data:", request.FILES)

        # Bind form data
        form = JobApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)  # Do not save yet
            application.vacancy = vacancy  # Assign the vacancy

            # ✅ Match `User` based on Django's built-in auth system
            if request.user.is_authenticated:
                application.user = request.user  # Directly assign the logged-in user
            else:
                return JsonResponse({"success": False, "error": "User is not authenticated"}, status=403)

            application.save()  # Save after assigning user
            return JsonResponse({"success": True})

        # 🔍 Debugging: Log form errors
        print("Form Errors:", form.errors)

        return JsonResponse({"success": False, "errors": form.errors}, status=400)





class AppliedJobsListView(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = "Applied Job.html"
    context_object_name = "applications"

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
    # def get_queryset(self):
    #     # Check if the user is logged in via session
    #     user_id = self.request.session.get('user_id')
    #     if user_id:
    #         return JobApplication.objects.filter(user_id=user_id)
    #     return JobApplication.objects.none()




class DeleteApplicationView(DeleteView):
    model = JobApplication
    success_url = reverse_lazy("applied_jobs")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
