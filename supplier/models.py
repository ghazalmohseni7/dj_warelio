from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^0\d{10}$',
    message="Phone number must start with 0 and be exactly 11 digits."
)


# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, validators=[phone_regex])

    def __str__(self):
        return f'supplier: {self.phone}/{self.name}'
