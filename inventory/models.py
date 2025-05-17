from django.db import models
from product.models import Product
from warehouse.models import WareHouse


# Create your models here.
class Inventory(models.Model):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name='inventories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product', 'warehouse')
