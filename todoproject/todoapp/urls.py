from django.urls import path, include
from .views import TaskListView, CategoryListView, TaskDetailView

urlpatterns = [
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('qr_code/', include('qr_code.urls', namespace='qr_code')),



]