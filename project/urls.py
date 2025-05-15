from django.urls import include, path
from dj_warelio.routers import router
from project.views import ProjectViewSets

router.register(prefix='projectvs', viewset=ProjectViewSets, basename='project')
urlpatterns = [path('', include(router.urls))]
