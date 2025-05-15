from django.urls import include, path
from dj_warelio.routers import router
from category.views import CategoryViewSets

router.register(prefix='categoryvs', viewset=CategoryViewSets, basename='category')
urlpatterns = [path('', include(router.urls))]
