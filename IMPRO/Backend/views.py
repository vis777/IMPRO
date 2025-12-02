from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, View, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware, localtime, now, is_naive
from .forms import AdminLoginForm, EmployeeForm, DepartmentForm, AttendanceForm, JobVacancyForm, ProcessForm, JobRotationForm
from .models import Department, Employee, Attendance, JobVacancy, Process
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.http import JsonResponse
from django.core.files.storage import default_storage
from rest_framework.generics import ListAPIView
from Frontend.models import JobApplication
from .forms import JobApplicationStatusForm

# Create your views here.
class IndexPageView(View):
    template_name = "index.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 
        
class AdminPageView(TemplateView):
    template_name = "adminindex.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Count the number of Department and Employee
        context['department_count'] = Department.objects.count()
        context['employee_count'] = Employee.objects.count()
        # Fetch all jobs and pass to context
        context['jobs'] = JobVacancy.objects.all()  
        return context

class AdminLoginView(FormView):
    template_name = "AdminLogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy('adminpage')

    def form_valid(self, form):
        un = form.cleaned_data['user_name']
        pwd = form.cleaned_data['pass_word']
        user = User.objects.filter(username__contains=un).exists()
        if user:
            x = authenticate(username=un, password=pwd)
            if x is not None:
                login(self.request, x)
                self.request.session['username'] = un
                self.request.session['password'] = pwd
                messages.success(self.request, "Login successful")
                return super().form_valid(form)
            else:
                messages.error(self.request, "Invalid Username or Password")
        else:
            messages.error(self.request, "Invalid Username or Password")
        return redirect('admin_login')

class AdminLogoutView(View):
    def get(self, request, *args, **kwargs):
        if 'username' in request.session:
            del request.session['username']
        messages.success(request, "Logout successful")
        return redirect('index')

class AddDepartmentView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "admin/Add Department.html"
    success_url = reverse_lazy('add_department')

    def form_valid(self, form):
        messages.success(self.request, "Department added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add department. Please check the form.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = Employee.objects.all()
        return context

class DepartmentListView(ListView):
    model = Department
    template_name = 'admin/Add and manage Department.html'
    context_object_name = 'dep'

class DepartmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Department
    template_name = "admin/Edit Department.html"
    fields = ['name', 'description']
    success_url = reverse_lazy('manage_department')
    success_message = "Department updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['depa'] = self.get_object()  
        return context

class DepartmentDeleteView(DeleteView):
    model = Department
    success_url = reverse_lazy('manage_department')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class AddEmployeeView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "admin/Add Employee.html"
    success_url = reverse_lazy('add_employee')

    def form_valid(self, form):
        user_name = self.request.POST.get("username")
        password = self.request.POST.get("password")
        shift = self.request.POST.get("shift")  

        form.instance.UserNaMe = user_name
        form.instance.PassWoRd = password
        form.instance.shift = shift  

        messages.success(self.request, "Employee added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add employee. Please check the form.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all() 
        return context

class EmployeeListView(ListView):
    model = Employee
    template_name = 'admin/Add and Manage Employee.html'
    context_object_name = 'emp'
    paginate_by = 10

    def get_queryset(self):
        queryset = Employee.objects.select_related('department')

        
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(position__icontains=search_query) |
                Q(department__name__icontains=search_query)
            )

        
        sort_by = self.request.GET.get('sort', 'name') 
        if sort_by in ['name', 'position', 'department']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            department_id = request.GET.get('department_id')
            employees = Employee.objects.filter(department_id=department_id).values('id', 'name')
            return JsonResponse(list(employees), safe=False)
        

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort', 'name')
        context['departments'] = Department.objects.all()
        return context


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm  
    template_name = 'admin/Edit Employee.html'
    success_url = reverse_lazy('manage_employee')  

    def form_valid(self, form):
        employee = form.instance
        
        # Update username
        username = self.request.POST.get('username')
        if username:
            employee.UserNaMe = username
        # Update password securely (only if changed)
        password = self.request.POST.get('password')
        if password:
            employee.PassWoRd = password  
        # Update shift
        shift = self.request.POST.get('shift')
        if shift in dict(Employee.SHIFT_CHOICES):  # Validate shift choice
            employee.shift = shift
            
        # Handle Image Upload
        if 'image' in self.request.FILES:
            image = self.request.FILES['image']
            
            # Optional: Delete old image to prevent unnecessary storage usage
            if employee.image:
                default_storage.delete(employee.image.path)
                
            employee.image = image  

        employee.save()
        messages.success(self.request, "Employee updated successfully.")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empl'] = self.get_object()
        context['departments'] = Department.objects.all()
        return context



        


class EmployeeDeleteView(DeleteView):
    model = Employee
    success_url = reverse_lazy('manage_employee')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class MarkAttendanceView(View):
    template_name = 'admin/Mark Attendance.html'
    form_class = AttendanceForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.time = timezone.localtime(timezone.now()).time()  # Set time to current time
            attendance.save()
            return redirect(reverse_lazy('mark_attendance'))  # Redirect to refresh the page
        
        return render(request, self.template_name, {'form': form})

class AttendanceRecordView(View):
    template_name = 'admin/Attendance Record.html'

    def get(self, request):
        all_records = Attendance.objects.all().order_by('-date', '-time')

        # Group records by date
        records_by_date = {}
        for record in all_records:
            records_by_date.setdefault(record.date, []).append(record)

        sorted_dates = sorted(records_by_date.keys(), reverse=True)  # Sort dates (latest first)

        # Pagination logic
        page_number = int(request.GET.get('page', 1))  # Get page number from query parameter
        paginator = Paginator(sorted_dates, 1)  # Show one day's records per page

        try:
            current_date = paginator.page(page_number).object_list[0]  # Get the date for the current page
            records = records_by_date[current_date]  # Fetch records for that date
        except:
            current_date = None
            records = []

        context = {
            'records': records,
            'current_date': current_date,
            'paginator': paginator,
            'page_number': page_number,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        record_id = request.POST.get('record_id')
        if record_id:
            attendance = get_object_or_404(Attendance, id=record_id)
            attendance.delete()
        return redirect(reverse('attendance_records'))

class JobVacancyCreateView(View):
    template_name = 'admin/Job Posting.html'

    def get(self, request):
        form = JobVacancyForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = JobVacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list') 
        return render(request, self.template_name, {'form': form})

class JobVacancyListView(View):
    template_name = 'admin/Job List.html'

    def get(self, request):
        jobs = JobVacancy.objects.all().order_by('-posted_on')
        return render(request, self.template_name, {'jobs': jobs})

class JobVacancyDeleteView(View):
    def post(self, request, pk):
        job = get_object_or_404(JobVacancy, pk=pk)
        job.delete()
        return redirect('job_list')

class ProcessListView(ListView):
    model = Process
    template_name = 'admin/Project list.html'
    context_object_name = 'processes'

class ProcessCreateView(CreateView):
    model = Process
    form_class = ProcessForm
    template_name = 'admin/Assign Project.html'
    success_url = reverse_lazy('process_list')  # Modify this to the URL where you want to redirect after success

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get selected department from GET request
        selected_department = self.request.GET.get("department")
        employees = Employee.objects.none()  # Default to an empty queryset

        if selected_department:
            employees = Employee.objects.filter(department_id=selected_department)

        context["departments"] = Department.objects.all()
        context["employees"] = employees
        context["selected_department"] = selected_department

        return context

    def form_valid(self, form):
        # Handle the form submission and save
        form.save()
        return super().form_valid(form)

class ProcessDeleteView(DeleteView):
    model = Process
    success_url = reverse_lazy('process_list')
    template_name = 'admin/confirm_delete.html'

class JobRotationView(View):
    def get(self, request, employee_id):
        employee = get_object_or_404(Employee, id=employee_id)
        form = JobRotationForm(instance=employee)
        return render(request, "admin/Add JobRotation.html", {"form": form, "employee": employee})

    def post(self, request, employee_id):
        employee = get_object_or_404(Employee, id=employee_id)
        form = JobRotationForm(request.POST, instance=employee)

        if form.is_valid():
            rotation = form.save(commit=False)

            # ✅ Set rotation_date to current date when promoted
            rotation.rotation_date = now().date()
            rotation.save()

            # ✅ Add a success message
            messages.success(request, f"{employee.name} has been promoted successfully!")

            return redirect("manage_employee")  # ✅ Redirect to employee management

        return render(request, "admin/Add JobRotation.html", {"form": form, "employee": employee})

class JobUserListView(ListView):
    model = JobApplication
    template_name = "admin/job_user_list.html"
    context_object_name = "applications"

    def get_queryset(self):
        return JobApplication.objects.select_related('vacancy')

    def post(self, request, *args, **kwargs):
        application_id = request.POST.get("application_id")
        application = JobApplication.objects.get(id=application_id)
        form = JobApplicationStatusForm(request.POST, instance=application)

        if form.is_valid():
            form.save()
            messages.success(request, "Application status updated successfully.")
        else:
            messages.error(request, "Failed to update application status.")

        return redirect(reverse("job_user_list"))  # Redirect back to the list view

class JobApplicationUpdateView(UpdateView):
    model = JobApplication
    form_class = JobApplicationStatusForm
    template_name = 'admin/update_application_status.html'
    
    def form_valid(self, form):
        application = form.save(commit=False)
        application.save()
        messages.success(self.request, "Application status updated successfully.")
        return redirect('job_user_list', job_id=application.vacancy.id)