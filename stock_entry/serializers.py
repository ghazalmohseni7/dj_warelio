from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from stock_entry.models import StockEntry
from utils.user_serializer import UserSerializer, User
from product.serializers import ProductSerializer, Product
from warehouse.serializers import WareHouseSerializer, WareHouse


class StockEntrySerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    received_by_id = serializers.IntegerField(write_only=True)
    warehouse = WareHouseSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    received_by = UserSerializer(read_only=True)

    def validate_product_id(self, value):
        if value is None:
            return value
        if not Product.objects.filter(id=value).exists():
            raise ValidationError("Related Product does not exist.")
        return value

    def validate_warehouse_id(self, value):
        if value is None:
            return value
        if not WareHouse.objects.filter(id=value).exists():
            raise ValidationError("Related warehouse does not exist.")
        return value

    def validate_received_by_id(self, value):
        if value is None:
            return value
        if not User.objects.filter(id=value).exists():
            raise ValidationError("Related user does not exist.")
        return value

    class Meta:
        model = StockEntry
        fields = ['quantity', 'warehouse_id', 'product_id', 'received_by_id', 'warehouse', 'product', 'received_by']
