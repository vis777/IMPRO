from django import forms
from .models import JobApplication
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(),
#         min_length=8,
#         help_text="Password must be at least 8 characters long."
#     )

#     class Meta:
#         model = Register
#         fields = ['First_Name', 'Last_Name', 'Email', 'UserName', 'PassWord']

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if Register.objects.filter(email=email).exists():
#             raise ValidationError("This email is already in use.")
#         return email

#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         if Register.objects.filter(username=username).exists():
#             raise ValidationError("This username is already taken.")
#         return usernam

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean_email(self):
        email = self.cleaned_data.get("email")  # Match model field name
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")  # Match model field name
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username



# class CustomLoginForm(forms.Form):
#    username = forms.CharField(max_length=50)
#    password = forms.CharField(widget=forms.PasswordInput)

# class UpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = Register
#         fields = ["first_name", "last_name", "email", "phone"]
#         widgets = {
#             "first_name": forms.TextInput(attrs={"class": "form-control"}),
#             "last_Name": forms.TextInput(attrs={"class": "form-control"}),
#             "email": forms.EmailInput(attrs={"class": "form-control"}),
#             "phone": forms.TextInput(attrs={"class": "form-control"}),
#         }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [ 'first_name', 'last_name', 'email', 'phone', 'resume','current_position','experience','education','cover_letter','message']

    # def save(self, commit=True, user=None):
    #     application = super().save(commit=False)
    #     if user:
    #         application.user = user
    #     if commit:
    #         application.save()
    #     return application