from rest_framework.viewsets import ModelViewSet
from project.models import Project
from project.serializers import ProjectSerializer


# Create your views here.

class ProjectViewSets(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
