from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.serializers import ProductSerializer
from supplier.models import Supplier
from category.models import Category


# Create your views here.
class ProductViewSets(ModelViewSet):
    queryset = Product.objects.select_related('category').select_related('supplier').all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        supplier_id = request.data.get('supplier_id')
        category_id = request.data.get('category_id')
        get_object_or_404(Supplier, id=supplier_id)
        get_object_or_404(Category, id=category_id)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        supplier_id = request.data.get('supplier_id')
        category_id = request.data.get('category_id')
        get_object_or_404(Supplier, id=supplier_id)
        get_object_or_404(Category, id=category_id)
        return super().update(request, *args, **kwargs)
