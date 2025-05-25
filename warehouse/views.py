from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from warehouse.models import WareHouse
from warehouse.serializers import WareHouseSerializer
from project.models import Project
from warehouse.permissions import WareHousePermissions


# Create your views here.
class WareHouseViewSets(ModelViewSet):
    queryset = WareHouse.objects.select_related('project').select_related('manager').all()
    serializer_class = WareHouseSerializer
    permission_classes = [IsAuthenticated, WareHousePermissions]

    def create(self, request, *args, **kwargs):
        project_id = request.data.get('project_id')
        manager_id = request.data.get('manager_id')
        get_object_or_404(Project, id=project_id)
        get_object_or_404(User, id=manager_id)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        project_id = request.data.get('project_id')
        manager_id = request.data.get('manager_id')
        get_object_or_404(Project, id=project_id)
        get_object_or_404(User, id=manager_id)
        return super().update(request, *args, **kwargs)
