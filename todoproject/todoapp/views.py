from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Task, Category


# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = ('todoapp/task-list.html')
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        my_tasks = Task.objects.all()
        return my_tasks

class TaskDetailView(DetailView):
    model = Task
    template_name = 'todoapp/task-detail.html'
    context_object_name = "task"
    

class CategoryListView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        cats = Category.objects.all()
        return cats




