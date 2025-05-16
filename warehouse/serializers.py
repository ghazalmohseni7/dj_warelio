from rest_framework import serializers
from warehouse.models import WareHouse
from project.serializers import ProjectSerializer


class WareHouseSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = WareHouse
        fields = ['name', 'location', 'project_id', 'user_id', 'project']
