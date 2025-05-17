from django.urls import path, include
from dj_warelio.routers import router
from inventory.views import InventoryViewSets

router.register(prefix='inventoryvs', viewset=InventoryViewSets, basename='inventory')
urlpatterns = [path('', include(router.urls))]
