from django.urls import path
from .views import OpenRouterChatView

urlpatterns = [
    path('wish/', OpenRouterChatView.as_view(), name='wish-qr'),

]