from django.urls import path, include
from dj_warelio.routers import router
from warehouse.views import WareHouseViewSets

router.register(prefix='warehouevs', viewset=WareHouseViewSets, basename='warehouse')
urlpatterns = [path('', include(router.urls))]
