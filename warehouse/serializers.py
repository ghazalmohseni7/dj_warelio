from rest_framework import serializers
from warehouse.models import WareHouse
from project.serializers import ProjectSerializer
from utils.user_serializer import UserSerializer


class WareHouseSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    manager_id = serializers.IntegerField(write_only=True)
    project = ProjectSerializer(read_only=True)
    manager = UserSerializer(read_only=True)

    class Meta:
        model = WareHouse
        fields = ['name', 'location', 'project_id', 'manager_id', 'project', 'manager']
