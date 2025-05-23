from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from stock_request.models import StockRequest, StockRequestItem
from utils.user_serializer import UserSerializer, User
from warehouse.serializers import WareHouseSerializer, WareHouse
from product.serializers import ProductSerializer, Product
from inventory.models import Inventory


class StockRequestSerializer(serializers.ModelSerializer):
    warehouse = WareHouseSerializer(read_only=True)
    requested_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    requested_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    warehouse_id = serializers.IntegerField(write_only=True)
    requested_by_id = serializers.IntegerField(write_only=True)
    approved_by_id = serializers.IntegerField(write_only=True)
    is_complete = serializers.BooleanField()

    class Meta:
        model = StockRequest
        fields = ['id', 'warehouse', 'warehouse_id', 'requested_by', 'requested_by_id', 'approved_by', 'approved_by_id',
                  'status', 'requested_at', 'is_complete']

    def validate_warehouse_id(self, value):
        if value is None:
            return value
        if not WareHouse.objects.filter(id=value).exists():
            raise ValidationError("Related warehouse does not exist.")
        return value

    def validate_requested_by_id(self, value):
        if value is None:
            return value
        if not User.objects.filter(id=value).exists():
            raise ValidationError("Related user does not exist.")
        return value

    def validate_approved_by_id(self, value):
        if value is None:
            return value
        if not User.objects.filter(id=value).exists():
            raise ValidationError("Related user does not exist.")
        return value


class StockRequestItemSerializer(serializers.ModelSerializer):
    stock_request = StockRequestSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    stock_request_id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StockRequestItem
        fields = ['id', 'quantity', 'stock_request_id', 'product_id', 'stock_request', 'product']

    def validate_product_id(self, value):
        if value is None:
            return value

        try:
            stock_request = StockRequest.objects.get(id=self.context['stock_request_id'])
        except StockRequest.DoesNotExist:
            raise ValidationError("Invalid stock request.")

        warehouse = stock_request.warehouse

        try:
            inventory = Inventory.objects.get(
                warehouse_id=warehouse.id,
                product_id=value,
                quantity__gt=0
            )
        except Inventory.DoesNotExist:
            raise ValidationError("Product is not available in the selected warehouse.")

        requested_quantity = int(self.initial_data.get('quantity', 0))
        if inventory.quantity < requested_quantity:
            raise ValidationError(
                f"There are only {inventory.quantity} units left, but you requested {requested_quantity}."
            )

        return value

    def validate_quantity(self, value):
        if self.context['method'] == 'POST':
            if value < 0:
                raise ValidationError('for create you can not enter negative quantity')

        return value

    def create(self, validated_data):
        return StockRequestItem.objects.create(stock_request_id=self.context['stock_request_id'], **validated_data)


class ActionStatusSerializer(serializers.Serializer):
    ACTION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    action = serializers.ChoiceField(choices=ACTION_CHOICES, write_only=True)
    status = serializers.CharField(read_only=True)


class ActionIsCompleteSerializer(serializers.Serializer):
    ACTION_CHOICES = [
        ('true', 'True'),
    ]
    complete = serializers.ChoiceField(choices=ACTION_CHOICES, write_only=True)
    status = serializers.CharField(read_only=True)
