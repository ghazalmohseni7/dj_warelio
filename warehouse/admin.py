from django.contrib import admin
from warehouse.models import WareHouse


# Register your models here.
@admin.register(WareHouse)
class AdminWareHouse(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'project__name', 'manager__username']
    ordering = ['id', 'name', 'location', 'project__name', 'manager__username']
    autocomplete_fields = ['project', 'manager']
    search_fields = ['id', 'name']  # add for inventory
