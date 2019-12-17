from django.urls import path, include
from .views import all_products, product_detail, add_product, delete_product, edit_product

urlpatterns = [
    path('', all_products, name='products'),
    path('<product_id>', product_detail, name='product_detail'),
    path('manage/', add_product, name='add_product'),
    path('manage/edit/<product_id>/', edit_product, name='edit_product'),
    path('manage/delete/<product_id>/', delete_product, name='delete_product'),
]
