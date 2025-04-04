from django.contrib.auth.models import User
from django import forms
from .models import Project,Task,Profile
from django.utils import timezone
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
    def __init__(self,*args,**kwargs):
        super(TaskForm,self).__init__(*args,**kwargs)
        user_choices = [(user.id,user.username) for user in User.objects.all()]
        self.fields['assigned_to'].choices = user_choices
    class Meta:
        model=Task
        fields= ['task_name','task_description','completed','due_date','assigned_to']
        widgets = {
            'completed':forms.RadioSelect(),
            'due_date':forms.DateTimeInput({'type':'datetime-local'}),
            'assigned_to':forms.Select(),
        }
        

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)

    class Meta:
        model=Profile
        fields=['profile_image']

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        if hasattr(self.instance,'owner')and self.instance.owner:
            self.fields['first_name'].initial = self.instance.owner.first_name
            self.fields['last_name'].initial = self.instance.owner.last_name
            self.fields['username'].initial = self.instance.owner.username
        elif isinstance(self.instance, User):
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['username'].initial = self.instance.username
    def save(self,commit=True):
        profile = super().save(commit=False)
        user= profile.owner

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.save()
        profile.profile_image = self.cleaned_data.get('profile_image')
        if commit:
            profile.save()
        return profile

