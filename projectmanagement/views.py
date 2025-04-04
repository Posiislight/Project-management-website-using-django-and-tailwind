from django.shortcuts import render,redirect,get_object_or_404
from .forms import TaskForm,RegisterForm,LoginForm,ProjectForm,ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from .models import Task,Project,Profile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.utils.timezone import now
# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request,user)
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request,'register.html',{'form':form})

def login_user(request):
    if request.method == 'POST':
            form = LoginForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                form.add_error(None,"Invalid username or password")
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

def base(request):
    return render(request,'base.html')

@login_required
def home(request):
    user = request.user
    projects = Project.objects.filter(owner=request.user)
    total_projects = projects.count()
    total_completed_tasks = sum(project.completed_tasks for project in projects)
    project_data = []
    for project in projects:
        progress = project.progress()
        project_data.append({
            'id': project.id,
            'name':project.project_name,
            'progress':progress,
            'completed_tasks':project.completed_tasks,
            'total_tasks':project.total_tasks
        })
    context = {
        'user':user,
        'total_projects':total_projects,
        'total_completed_tasks':total_completed_tasks,
        'project_data':project_data,
        
    }
    return render(request,'index.html',context)

@login_required
def add_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('home')
    return render(request,'add_project.html',{'form':form})

@login_required
def edit_project(request,project_id):
    project = get_object_or_404(Project,id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectForm(instance=project)
    return render(request,'edit_project.html',{'form':form, 'project':project})

def delete_project(request,project_id):
    project = get_object_or_404(Project,id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('home')
    return render(request,'delete_project.html',{'project':project})
    
@login_required
def add_task(request,project_id):
    project = get_object_or_404(Project,id=project_id,owner=request.user)
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.owner = request.user
            task.save()
            return redirect('project_details',project_id=project.id)
    return render(request,'add_task.html',{'form':form,'project':project})

@login_required
def edit_task(request,task_id):
    task = get_object_or_404(Task,id=task_id)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        project = task.project
        if form.is_valid():
            form.save()
        return redirect('project_details', project_id=project.id)
    return render(request,'edit_task.html',{'form':form,'task':task})

@login_required
def project_details(request,project_id):
    project = get_object_or_404(Project,id=project_id)
    
    tasks= Task.objects.filter(project=project,owner=request.user)
    task_data = []
    task = tasks.first()
    for task in tasks:
        past_due_date = task.due_date and now() > task.due_date
        task.save()
        if task.past_due_date == True:
            task.past_due_date = 'Yes'
        elif task.past_due_date == False:
            task.past_due_date = 'No'
        task_data.append({
            'id' : task.id,
            'task_name':task.task_name,
            'task_description':task.task_description,
            'due_date':task.due_date,
            'past_due_date':task.past_due_date,
            'assigned_to':task.assigned_to
        })

    context = {
        'project':project,
        'task':tasks,
        'task_data':task_data,
    }
    return render(request,'project_details.html',context)

def edit_task(request,task_id,project_id):
    task = get_object_or_404(Task,id=task_id)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        project = task.project
        if form.is_valid():
            form.save()
        return redirect('project_details', project_id=project.id)
    return render(request,'edit_task.html',{'form':form,'task':task})

def delete_task(request,task_id,project_id):
    task = get_object_or_404(Task,id=task_id)
    project = task.project
    if request.method == 'POST':
        task.delete()
        return redirect('project_details',project_id = project.id)
    return render(request,'delete_task.html',{'task':task})

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout_user(request,user)
    return redirect('base')

@login_required
def profile(request,user_id):
    user = get_object_or_404(User,id=user_id)
    profile, created = Profile.objects.get_or_create(owner=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request,'profile_settings.html',{'form':form,'user':user})

def assigned_tasks(request):
    assigned_tasks = Task.objects.filter(assigned_to=request.user)
    return render(request,'assigned_tasks.html',{'assigned_tasks':assigned_tasks})