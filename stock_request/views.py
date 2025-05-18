from rest_framework.viewsets import ModelViewSet
from stock_request.models import StockRequest, StockRequestItem
from stock_request.serializers import StockRequestSerializer, StockRequestItemSerializer


# Create your views here.
class StockRequestViewSets(ModelViewSet):
    queryset = StockRequest.objects.select_related('warehouse', 'requested_by', 'approved_by').all()
    serializer_class = StockRequestSerializer


class StockRequestItemViewSets(ModelViewSet):
    serializer_class = StockRequestItemSerializer

    def get_queryset(self):
        stock_request_id = self.kwargs['stock_request_pk_pk']
        queryset = StockRequestItem.objects.select_related('stock_request', 'product').filter(
            stock_request_id=stock_request_id)
        return queryset

    def get_serializer_context(self):
        stock_request_id = self.kwargs['stock_request_pk_pk']
        return {'stock_request_id': stock_request_id}
