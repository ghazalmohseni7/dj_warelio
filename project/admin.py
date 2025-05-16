from django.contrib import admin
from project.models import Project


# Register your models here.
@admin.register(Project)
class AdminProject(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id', 'name']
    search_fields = ['name']
