from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from supplier.models import Supplier
from supplier.serializers import SupplierSerializer
from supplier.permissions import SupplierPermissions


# Create your views here.

class SupplierViewSets(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, SupplierPermissions]
