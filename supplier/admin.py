from django.contrib import admin
from supplier.models import Supplier


# Register your models here.
@admin.register(Supplier)
class AdminSupplier(admin.ModelAdmin):
    list_display = ['id', 'phone', 'name']
    ordering = ['id', 'phone', 'name']
    search_fields = ['phone', 'name']
