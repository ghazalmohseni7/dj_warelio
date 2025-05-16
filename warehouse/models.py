from django.db import models
from project.models import Project


# Create your models here.
class WareHouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, null=False, blank=False)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='warehouses')

    def __str__(self):
        return f'{self.name} - {self.project.name}'
