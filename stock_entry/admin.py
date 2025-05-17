from django.contrib import admin
from stock_entry.models import StockEntry


# Register your models here.
@admin.register(StockEntry)
class AdminStockEntry(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'received_at', 'warehouse__id', 'warehouse__name', 'product__id', 'product__name',
                    'received_by__id','received_by__username']
    ordering = ['id', 'quantity', 'received_at', 'warehouse__id', 'warehouse__name', 'product__id', 'product__name',
                'received_by__id', 'received_by__username']
    autocomplete_fields = ['warehouse', 'product', 'received_by']
