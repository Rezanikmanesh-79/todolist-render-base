from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.TaskUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete'),
    path('complete/<int:task_id>/', views.complete_task, name='complete'),
    path('task-report/', views.user_task_report, name='task-report'),
]
