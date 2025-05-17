from django.db import models
from django.contrib.auth.models import User
from warehouse.models import WareHouse
from product.models import Product


# Create your models here.

class StockRequest(models.Model):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name='stock_requests')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_requests_made')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='stock_requests_approved')

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request #{self.id} by {self.requested_by}"


class StockRequestItem(models.Model):
    stock_request = models.ForeignKey(StockRequest, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
