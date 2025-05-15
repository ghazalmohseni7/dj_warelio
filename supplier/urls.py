from django.urls import path, include
from dj_warelio.routers import router
from supplier.views import SupplierViewSets

router.register(prefix='suppliervs', viewset=SupplierViewSets, basename='supplier')
urlpatterns = [path('', include(router.urls))]
