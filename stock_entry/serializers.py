from rest_framework import serializers
from stock_entry.models import StockEntry
from utils.user_serializer import UserSerializer
from product.serializers import ProductSerializer
from warehouse.serializers import WareHouseSerializer


class StockEntrySerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    received_by_id = serializers.IntegerField(write_only=True)
    warehouse = WareHouseSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    received_by = UserSerializer(read_only=True)

    class Meta:
        model = StockEntry
        fields = ['quantity', 'warehouse_id', 'product_id', 'received_by_id', 'warehouse', 'product', 'received_by']
