from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from warehouse.models import WareHouse
from warehouse.serializers import WareHouseSerializer
from project.models import Project


# Create your views here.
class WareHouseViewSets(ModelViewSet):
    queryset = WareHouse.objects.select_related('project').all()
    serializer_class = WareHouseSerializer

    def create(self, request, *args, **kwargs):
        project_id = request.data.get('project_id')
        get_object_or_404(Project, id=project_id)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        project_id = request.data.get('project_id')
        get_object_or_404(Project, id=project_id)
        return super().update(request, *args, **kwargs)
