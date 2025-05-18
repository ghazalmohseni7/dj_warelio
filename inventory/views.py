from rest_framework.viewsets import ModelViewSet
from inventory.models import Inventory
from inventory.serializers import InventorySerializer


# Create your views here.

class InventoryViewSets(ModelViewSet):
    http_method_names = ['get']
    queryset = Inventory.objects.select_related('product').select_related('warehouse').all()
    serializer_class = InventorySerializer
