from django.contrib import admin
from warehouse.models import WareHouse


# Register your models here.
@admin.register(WareHouse)
class AdminWareHouse(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'project__name']
    ordering = ['id', 'name', 'location', 'project__name']
