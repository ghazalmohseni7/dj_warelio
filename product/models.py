from django.db import models
from supplier.models import Supplier
from category.models import Category


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='products')

    def __str__(self):
        return f'Product "{self.name}" (Code: {self.code}) - Price: {self.price}'
