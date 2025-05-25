from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from stock_entry.models import StockEntry
from stock_entry.serializers import StockEntrySerializer
from inventory.models import Inventory
from stock_entry.permissions import SEPermissions


# Create your views here.

class StockEntryViewSets(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = StockEntry.objects.select_related('warehouse').select_related('product').select_related(
        'received_by').all()
    serializer_class = StockEntrySerializer
    permission_classes = [IsAuthenticated, SEPermissions]

    def perform_create(self, serializer):
        stock_entry = serializer.save()  # negah dar ino
        inventory, created = Inventory.objects.get_or_create(warehouse=stock_entry.warehouse,
                                                             product=stock_entry.product,
                                                             defaults={
                                                                 'quantity': stock_entry.quantity})  # if it is created then use this value
        if not created:
            inventory.quantity += stock_entry.quantity
            inventory.save()
