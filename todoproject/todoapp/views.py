from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .forms import CategoryForm, TaskForm
from .models import Task, Category


# Create your views here.

def index(request):
    categories = Category.objects.all()
    return render(request, 'todoapp/index.html',
                  {'categories': categories})

def task_view(request, pk):
    cat_tasks = Task.objects.filter(category_id=pk).filter(complete=False)
    category = Category.objects.get(id=pk)
    return render(request, 'todoapp/task-list.html',
                  {'cat_tasks': cat_tasks, 'category': category},)

class TaskDetailView(DetailView):
    model = Task
    template_name = 'todoapp/task-detail.html'
    context_object_name = "task"
    

def task_del_view(request, pk):
    cat_task = Task.objects.get(pk=pk)
    cat_task.complete = True
    cat_task.save()
    c_id = cat_task.category.id
    return redirect(task_view, pk=c_id)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')  #может быть заменить на (home)
    else:
        form = CategoryForm()
        context = {'form': form}
        return render(request, 'todoapp/add-category.html', context)

def add_task(request, cat_id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = Category.objects.get(id=cat_id)
            post.save()
        return redirect(task_view, pk=post.category.id)
    else:
        form = TaskForm()
        context = {'form': form}
    return render(request, 'todoapp/add-task.html', context)

def category_del(request, c_id):
    category = Category.objects.get(id=c_id)
    category.delete()
    return redirect('home')

