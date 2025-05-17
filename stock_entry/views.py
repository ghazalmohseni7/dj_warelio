from rest_framework.viewsets import ModelViewSet
from stock_entry.models import StockEntry
from stock_entry.serializers import StockEntrySerializer


# Create your views here.

class StockEntryViewSets(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = StockEntry.objects.select_related('warehouse').select_related('product').select_related(
        'received_by').all()
    serializer_class = StockEntrySerializer
