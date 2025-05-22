from django_filters import FilterSet
from inventory.models import Inventory


class InventoryFilter(FilterSet):
    class Meta:
        model = Inventory
        fields = {'warehouse__id': ['exact']}
