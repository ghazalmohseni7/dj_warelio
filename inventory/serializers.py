from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from inventory.models import Inventory
from product.serializers import ProductSerializer
from warehouse.serializers import WareHouseSerializer
from warehouse.models import WareHouse
from product.models import Product


class InventorySerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    warehouse = WareHouseSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'quantity', 'warehouse_id', 'product_id', 'warehouse', 'product']

    def validate_warehouse_id(self, value):
        if value is None:
            return value
        if not WareHouse.objects.filter(id=value).exists():
            raise ValidationError("Related warehouse does not exist.")
        return value

    def validate_product_id(self, value):
        if value is None:
            return value
        if not Product.objects.filter(id=value).exists():
            raise ValidationError("Related product does not exist.")
        return value


class SummarySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    product = ProductSerializer()
    warehouse = WareHouseSerializer()

