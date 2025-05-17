from django.db import models
from django.contrib.auth.models import User
from warehouse.models import WareHouse
from product.models import Product


# Create your models here.
class StockEntry(models.Model):
    warehouse = models.ForeignKey(to=WareHouse, on_delete=models.CASCADE, related_name='stock_entries')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='stock_entries')
    quantity = models.PositiveIntegerField()
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_entries_received')
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.quantity} of {self.product.name} received at {self.warehouse.name} "
            f"by {self.received_by.username if self.received_by else 'Unknown'} "
            f"on {self.received_at.strftime('%Y-%m-%d %H:%M')}"
        )
