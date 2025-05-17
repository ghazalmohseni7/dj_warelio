from rest_framework.viewsets import ModelViewSet
from inventory.models import Inventory
from inventory.serializers import InventorySerializer
# Create your views here.

class InventoryViewSets(ModelViewSet):
    queryset = Inventory.objects.select_related('product').select_related('warehouse').all()
    serializer_class = InventorySerializer