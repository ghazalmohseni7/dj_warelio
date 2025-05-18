from rest_framework import serializers
from product.models import Product
from supplier.serializers import SupplierSerializer
from category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    supplier_id = serializers.IntegerField(write_only=True)
    supplier = SupplierSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'description', 'price', 'category_id', 'supplier_id', 'supplier', 'category']
