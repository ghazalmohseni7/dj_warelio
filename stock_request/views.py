from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from stock_request.models import StockRequest, StockRequestItem
from stock_request.serializers import StockRequestSerializer, StockRequestItemSerializer


# Create your views here.
class StockRequestViewSets(ModelViewSet):
    http_method_names = ['get']
    queryset = StockRequest.objects.select_related('warehouse', 'requested_by', 'approved_by').all()
    serializer_class = StockRequestSerializer

    @action(detail=True, methods=['patch'], url_path='complete')
    def complete_stock_request(self, request, pk=None):
        obj = get_object_or_404(StockRequest, id=pk)
        is_complete = request.query_params.get('is_complete')

        if is_complete in ['true', '1', 'True']:
            if obj.is_complete:
                return Response({'error': 'This request is already being processed and completed`'}, status=400)
            else:
                StockRequest.objects.filter(id=pk).update(is_complete=True)
                # call the task that sends info
            return Response({'status': 'Marked complete'}, status=200)
        else:
            return Response({'error': 'Invalid or missing `is_complete`'}, status=400)


class StockRequestItemViewSets(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch']
    serializer_class = StockRequestItemSerializer

    def get_queryset(self):
        stock_request_id = self.kwargs['stock_request_pk_pk']
        queryset = StockRequestItem.objects.select_related('stock_request', 'product').filter(
            stock_request_id=stock_request_id
        )

        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            queryset = queryset.filter(
                stock_request__is_complete=False,
                stock_request__status='pending'
            )

        return queryset

    def get_serializer_context(self):
        stock_request_id = self.kwargs['stock_request_pk_pk']
        method = self.request.method
        return {'stock_request_id': stock_request_id, 'method': method}

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.quantity += serializer.validated_data['quantity']
        instance.save()

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
