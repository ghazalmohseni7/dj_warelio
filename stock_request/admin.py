from django.contrib import admin
from stock_request.models import StockRequest, StockRequestItem


# Register your models here.


class StockRequestItemInline(admin.TabularInline):
    model = StockRequestItem
    extra = 1
    min_num = 1
    autocomplete_fields = ['product']
    fields = ['product', 'quantity']


@admin.register(StockRequest)
class StockRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'warehouse', 'requested_by', 'approved_by', 'status', 'requested_at']
    list_filter = ['status', 'warehouse']
    search_fields = ['requested_by__username', 'approved_by__username']
    autocomplete_fields = ['warehouse', 'requested_by', 'approved_by']
    inlines = [StockRequestItemInline]
    readonly_fields = ['requested_at', ]


@admin.register(StockRequestItem)
class StockRequestItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock_request', 'product', 'quantity']
    search_fields = ['product__name', ]
    autocomplete_fields = ['stock_request', 'product']
