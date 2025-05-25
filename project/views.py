from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from project.models import Project
from project.serializers import ProjectSerializer
from project.permissions import ProjectPermissions


# Create your views here.

class ProjectViewSets(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermissions]
