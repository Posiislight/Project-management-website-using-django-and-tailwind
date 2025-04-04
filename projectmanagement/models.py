from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import now
# Create your models here.

class Project(models.Model):
    choice_field = [
        (True,'Yes'),
        (False,'No')
    ]
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    project_description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    total_tasks = models.PositiveIntegerField(default=0)
    completed_tasks = models.PositiveIntegerField(default=0)
    past_due_date = models.BooleanField(default=False,choices=choice_field)

    def __str__(self):
        return self.project_name
    
    def progress(self):
        if self.total_tasks == 0:
            return 0
        return (self.completed_tasks/self.total_tasks)*100

class Task(models.Model):
    choice_field = [
        (True,'Yes'),
        (False,'No'),
    ]
    owner = models.ForeignKey(User,on_delete= models.CASCADE)
    project = models.ForeignKey(Project,related_name = 'tasks',on_delete= models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_description = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False,choices=choice_field)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(default=timezone.now)
    past_due_date = models.BooleanField(default=False,choices=choice_field)
    assigned_by = models.ForeignKey(User,related_name='assigned_by',on_delete=models.SET_NULL,null=True,blank=True)
    assigned_to = models.ForeignKey(User,related_name='assigned_to',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.task_name

class Profile(models.Model):
    owner = models.OneToOneField(User,related_name = 'profile',on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to = 'profile_images/')

    def __str__(self):
        return str(self.id)

@receiver(post_save,sender=Task)
def update_task_counts_on_save(sender,instance,**kwargs):
    project = instance.project
    project.total_tasks = project.tasks.count()
    project.completed_tasks = project.tasks.filter(completed=True).count()
    project.save()

@receiver(post_delete,sender=Task)
def update_task_counts_delete(sender,instance,**kwargs):
    project = instance.project
    project.total_tasks = project.tasks.count()
    project.completed_tasks = project.tasks.filter(completed=True).count()
    project.save()

@receiver(post_save,sender=User)
def createprofile(sender,instance,created,**kwargs):
    if created:
        Profile.object.create(owner=instance)

