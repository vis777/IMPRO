from django import forms
from django.utils.timezone import now
from .models import Employee, Department, Attendance, JobVacancy, Process
from Frontend.models import JobApplication

class AdminLoginForm(forms.Form):
    user_name = forms.CharField(max_length=100, label="Username")
    pass_word = forms.CharField(widget=forms.PasswordInput, label="Password")

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

class EmployeeForm(forms.ModelForm):
    shift = forms.ChoiceField(choices=Employee.SHIFT_CHOICES, required=True, label="Shift")

    class Meta:
        model = Employee
        fields = ['name', 'UserNaMe', 'PassWoRd', 'email', 'phone', 'department', 'location', 'position', 'date_joined', 'salary', 'status', 'shift', 'image', 'rotation_date', 'reason']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'time', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        
        # Get today's date
        today = now().date()

        # Filter employees who haven't marked attendance today
        self.fields['employee'].queryset = Employee.objects.exclude(
            id__in=Attendance.objects.filter(date=today).values_list('employee', flat=True)
        )

class JobVacancyForm(forms.ModelForm):
    class Meta:
        model = JobVacancy
        fields = ['title', 'description', 'qualifications', 'location', 'salary']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'qualifications': forms.Textarea(attrs={'rows': 3}),
        }

class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['name', 'description', 'department', 'assigned_to', 'start_date', 'due_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_to': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ProcessForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = Employee.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['assigned_to'].queryset = Employee.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and use an empty queryset
        elif self.instance.pk:
            self.fields['assigned_to'].queryset = self.instance.department.employee_set.all()

class JobRotationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["position", "salary", "shift", "reason", "rotation_date"]
        widgets = {
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "salary": forms.NumberInput(attrs={"class": "form-control"}),
            "shift": forms.Select(choices=[("day", "Day"), ("night", "Night")], attrs={"class": "form-control"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "rotation_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}), 
        }

class JobApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status', 'message']

    status = forms.ChoiceField(choices=JobApplication.STATUS_CHOICES, required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), required=False)
# class JobRotationForm(forms.Form):
#     to_role = forms.CharField(label="New Role", max_length=100)
#     new_salary = forms.DecimalField(label="New Salary", max_digits=10, decimal_places=2)
    
#     shift_rotation = forms.ChoiceField(
#         label="Shift Rotation",
#         choices=[("day", "Day Shift"), ("night", "Night Shift")],
#         required=True
#     )
    
#     reason = forms.CharField(label="Reason", widget=forms.Textarea, required=False)
#     rotation_date = forms.DateField(label="Rotation Date", widget=forms.DateInput(attrs={"type": "date"}))

#     def __init__(self, *args, **kwargs):
#         self.employee = kwargs.pop("employee", None)
#         super().__init__(*args, **kwargs)

#         # ✅ Set default shift from employee data if available
#         if self.employee:
#             self.fields["shift_rotation"].initial = self.employee.shift or "day"
