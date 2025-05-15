from rest_framework.viewsets import ModelViewSet
from supplier.models import Supplier
from supplier.serializers import SupplierSerializer


# Create your views here.

class SupplierViewSets(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
