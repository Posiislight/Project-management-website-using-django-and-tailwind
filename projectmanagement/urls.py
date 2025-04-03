from django.urls import path
from . import views  # Correct import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.base, name='base'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/<int:project_id>/add-task/', views.add_task, name='add_task'),
    path('task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('projects/<int:project_id>/',views.edit_project,name='edit_project'),
    path('projects/<int:project_id>/delete-project/',views.delete_project,name='delete_project'),
    path('projects/<int:project_id>/project-details/',views.project_details,name='project_details'),
    path('task/<int:task_id>/<int:project_id>/edit_task/',views.edit_task,name='edit_task'),
    path('task/<int:task_id>/<int:project_id>/delete_task/',views.delete_task,name='delete_task'),
    path('profile/<int:user_id>/',views.profile,name='profile'),
    path('logout/',views.login_user,name='logout')
]

