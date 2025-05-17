from django.contrib import admin
from inventory.models import Inventory


# Register your models here.
@admin.register(Inventory)
class AdminInventory(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'warehouse__id', 'warehouse__name', 'product__id', 'product__name']
    ordering = ['id', 'quantity', 'warehouse__id', 'warehouse__name', 'product__id', 'product__name']
    autocomplete_fields = ['warehouse', 'product']
