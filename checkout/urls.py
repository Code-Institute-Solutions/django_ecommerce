from django.urls import path, include
from .views import checkout, checkout_success

urlpatterns = [
    path('', checkout, name='checkout'),
    path('checkout_successs/<order_number>/', checkout_success, name='checkout_success'),
]