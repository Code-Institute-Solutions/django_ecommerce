from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

admin.site.register(Product, ProductAdmin)