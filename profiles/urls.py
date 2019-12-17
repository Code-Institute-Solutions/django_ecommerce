from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>/', views.order_history, name='order_history')
]