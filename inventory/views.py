from django.db.models.aggregates import Sum
from django.forms.models import model_to_dict
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from inventory.models import Inventory
from inventory.serializers import InventorySerializer, SummarySerializer
from product.serializers import ProductSerializer, Product
from warehouse.serializers import WareHouseSerializer, WareHouse


# Create your views here.

class InventoryViewSets(ModelViewSet):
    http_method_names = ['get']
    queryset = Inventory.objects.select_related('product').select_related('warehouse').all()
    serializer_class = InventorySerializer

    @action(detail=False, methods=['get'], url_path='summary_items')
    def summary_items(self, request):
        warehouse_id = request.query_params.get('warehouse_id')
        product_id = request.query_params.get('product_id')
        qs = self.queryset

        if warehouse_id:
            qs = qs.filter(warehouse_id=warehouse_id)
            summary = qs.values('product_id', 'warehouse_id').annotate(total_quantity=Sum('quantity')).order_by(
                'product_id')
        if product_id:
            qs = qs.filter(product_id=product_id)
            summary = qs.values('product_id', 'warehouse_id').annotate(total_quantity=Sum('quantity')).order_by(
                'product_id')
        if not product_id and not warehouse_id:
            summary = qs.values('product_id', 'warehouse_id').annotate(total_quantity=Sum('quantity')).order_by(
                'warehouse_id')

        product_map = {p.id: p for p in Product.objects.filter(id__in=[s['product_id'] for s in summary])}
        warehouse_map = {w.id: w for w in WareHouse.objects.filter(id__in=[s['warehouse_id'] for s in summary])}

        for item in summary:
            item['product'] = model_to_dict(product_map[item['product_id']])
            item['warehouse'] = model_to_dict(warehouse_map[item['warehouse_id']])

        serializer = SummarySerializer(data=summary, many=True)
        return Response(serializer.initial_data)
