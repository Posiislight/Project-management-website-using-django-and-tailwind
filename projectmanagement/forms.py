from django.contrib.auth.models import User
from django import forms
from .models import Project,Task
class RegisterForm(forms.ModelForm):
    class Meta:
        model= User
        fields= ['username','password','first_name','last_name']

class LoginForm(forms.ModelForm):
    class Meta:
        model= User
        fields= ['username','password']

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields= ['project_name','project_description']

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields= ['task_name','task_description','completed']
        widgets = {
            'completed':forms.RadioSelect()
        }