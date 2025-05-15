from django.contrib import admin
from category.models import Category


# Register your models here.
@admin.register(Category)
class AdminProject(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id', 'name']
