from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from category.models import Category
from category.serializers import CategorySerializer
from category.permissions import CategoryPermissions


# Create your views here.

class CategoryViewSets(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, CategoryPermissions]
