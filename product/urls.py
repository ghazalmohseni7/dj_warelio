from django.urls import path, include
from dj_warelio.routers import router
from product.views import ProductViewSets

router.register(prefix='productvs', viewset=ProductViewSets, basename='product')
urlpatterns = [path('', include(router.urls))]
