from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/edit', views.edit, name='edit'),
    path('post/<int:pk>/delete', views.delete, name='delete'),
]
