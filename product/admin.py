from django.contrib import admin
from product.models import Product


# Register your models here.
@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'code', 'price', 'category__name', 'supplier__name']
    ordering = ['name', 'code', 'price', 'category__name', 'supplier__name']
    autocomplete_fields = ['category', 'supplier']
