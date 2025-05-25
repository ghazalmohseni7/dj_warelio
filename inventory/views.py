from django.db.models.aggregates import Sum
from django.forms.models import model_to_dict
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from inventory.models import Inventory
from inventory.serializers import InventorySerializer, SummarySerializer
from product.serializers import ProductSerializer, Product
from warehouse.serializers import WareHouseSerializer, WareHouse
from inventory.filters import InventoryFilter


# Create your views here.

class InventoryViewSets(ModelViewSet):
    http_method_names = ['get']
    queryset = Inventory.objects.select_related('product').select_related('warehouse').all()
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventoryFilter
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Summarize inventory quantities grouped by product and warehouse.",
        parameters=[
            OpenApiParameter(
                name="warehouse_id",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter by warehouse ID"
            ),
            OpenApiParameter(
                name="product_id",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter by product ID"
            ),
            # remove filtering and ordering fields from swagger
            OpenApiParameter(name="warehouse__id", exclude=True),
        ],
        responses={
            200: SummarySerializer(many=True),
            400: OpenApiExample(
                "Invalid filter input",
                value={"detail": "Bad request"},
                response_only=True,
                status_codes=["400"]
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='summary_items')
    def summary_items(self, request):
        warehouse_id = request.query_params.get('warehouse_id')
        product_id = request.query_params.get('product_id')
        qs = self.queryset

        # option 1
        if warehouse_id:
            qs = qs.filter(warehouse_id=warehouse_id)

        if product_id:
            qs = qs.filter(product_id=product_id)

        summary = qs.values('product_id', 'warehouse_id').annotate(total_quantity=Sum('quantity')).order_by(
            'warehouse_id')

        product_map = {p.id: p for p in Product.objects.filter(id__in=[s['product_id'] for s in summary])}
        warehouse_map = {w.id: w for w in WareHouse.objects.filter(id__in=[s['warehouse_id'] for s in summary])}

        for item in summary:
            item['product'] = model_to_dict(product_map[item['product_id']])
            item['warehouse'] = model_to_dict(warehouse_map[item['warehouse_id']])

        serializer = SummarySerializer(data=summary, many=True)
        return Response(serializer.initial_data)

        # option 2 , more optimized but you cant use the nested serializer

        # x = qs.values('product__name', 'warehouse', 'product_id', 'warehouse_id').annotate(
        #     total_quantity=Sum('quantity'))
