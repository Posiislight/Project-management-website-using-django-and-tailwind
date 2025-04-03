from django.contrib import admin
from .models import Profile,Task,Project

# Register your models here.
admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Project)