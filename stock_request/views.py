from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from stock_request.models import StockRequest, StockRequestItem
from stock_request.serializers import StockRequestSerializer, StockRequestItemSerializer, ActionStatusSerializer, \
    ActionIsCompleteSerializer
from pubsub.publisher import publish
from inventory.models import Inventory
from utils.action_data_deserializer import deserialize
from stock_request.permissions import SRIPermissions, SRPermissions


# Create your views here.
class StockRequestViewSets(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = StockRequest.objects.select_related('warehouse', 'requested_by', 'approved_by').all()
    permission_classes = [IsAuthenticated, SRPermissions]

    def get_serializer_class(self):
        if self.action == 'approve_stock_request':
            return ActionStatusSerializer
        elif self.action == 'complete_stock_request':
            return ActionIsCompleteSerializer
        else:
            return StockRequestSerializer

    @action(detail=True, methods=['post'], url_path='complete', url_name='complete')
    def complete_stock_request(self, request, pk=None):
        obj = get_object_or_404(StockRequest.objects.select_related('warehouse'), id=pk)

        # deserializer
        is_complete = deserialize(data=request.data, serializer=ActionIsCompleteSerializer)['complete']

        if is_complete == 'True':
            if obj.is_complete:
                return Response({'status': 'This request is already being processed and completed`'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                obj.is_complete = True
                obj.save(update_fields=['is_complete'])

                # call the task that sends info
                publish({'stock_request_id': pk, 'warehouse_id': obj.warehouse_id})
                return Response({'status': 'Marked complete'}, status=status.HTTP_200_OK)
        return Response({'status': 'Marked complete'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='approve', url_name='approve')
    @transaction.atomic
    def approve_stock_request(self, request, pk=None):
        stock_request = get_object_or_404(StockRequest.objects.select_related('warehouse'), id=pk)

        # deserializer
        status_ = deserialize(data=request.data, serializer=ActionStatusSerializer)['action']

        if status_ == 'approve':
            stock_request.status = 'approved'
            # stock_request.approved_by = request.user
            stock_request.save(update_fields=['status', 'approved_by'])

            items = stock_request.items.select_related('product')
            for item in items:

                inventory = get_object_or_404(
                    Inventory,
                    warehouse_id=stock_request.warehouse_id,
                    product_id=item.product_id
                )
                if inventory.quantity < item.quantity:
                    stock_request.status = 'rejected'
                    # stock_request.approved_by = request.user
                    stock_request.save(update_fields=['status', 'approved_by'])

                    return Response(
                        {
                            'status': 'rejected',
                            'error': f'Insufficient inventory for product {item.product.name}'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                inventory.quantity -= item.quantity
                inventory.save()

            return Response({'status': 'approved'}, status=status.HTTP_200_OK)
        else:
            stock_request.status = 'rejected'
            # stock_request.approved_by = request.user
            stock_request.save(update_fields=['status', 'approved_by'])
            return Response({'status': 'rejected'}, status=status.HTTP_200_OK)


class StockRequestItemViewSets(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch']
    serializer_class = StockRequestItemSerializer
    permission_classes = [IsAuthenticated, SRIPermissions]

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
