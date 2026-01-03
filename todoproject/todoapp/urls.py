from django.urls import path, include

from . import views
from .views import TaskDetailView, task_view, task_del_view, add_category, add_task, category_del

urlpatterns = [
    path('task/<int:pk>/del/', task_del_view, name='task-del'),
    path('tasks/<int:pk>/', task_view, name='task-list'),
    path('taskdetail/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('qr_code/', include('qr_code.urls', namespace='qr_code')),
    path('add_category/', add_category, name='add-c'),
    path('add_task/<int:cat_id>/', add_task, name='add-task'),
    path('category/<int:c_id>/del', category_del, name='c-del'),

]