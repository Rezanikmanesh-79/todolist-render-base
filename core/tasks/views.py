from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Task
from .form import TaskForm 
from django.contrib.auth.models import User

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # یوزر فقط برای خودش تسک می‌سازد
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('list')

    def test_func(self):
        return self.request.user == self.get_object().user or self.request.user.is_superuser  # یوزر فقط تسک خودش را ویرایش کند

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('list')

    def test_func(self):
        return self.request.user == self.get_object().user or self.request.user.is_superuser  # یوزر فقط تسک خودش را حذف کند

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user == task.user or request.user.is_superuser:
        task.is_completed = True
        task.save()
    return redirect('list')

@login_required
def user_task_report(request):
    if not request.user.is_superuser:
        return redirect('list') 
    
    users = User.objects.all()
    user_data = []

    for user in users:
        total_tasks = Task.objects.filter(user=user).count()
        completed_tasks = Task.objects.filter(user=user, is_completed=True).count()
        user_data.append({'user': user, 'total': total_tasks, 'completed': completed_tasks})

    return render(request, 'tasks/user_task_report.html', {'user_data': user_data})
