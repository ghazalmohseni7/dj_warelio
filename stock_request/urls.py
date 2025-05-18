from django.urls import path, include
from rest_framework_nested import routers as nested_router
from dj_warelio.routers import router
from stock_request.views import StockRequestViewSets, StockRequestItemViewSets

router.register(prefix='stock_requstvs', viewset=StockRequestViewSets, basename='stock_requst')
stock_request_nested_router = nested_router.NestedDefaultRouter(parent_router=router, parent_prefix='stock_requstvs',
                                                                lookup='stock_request_pk')
stock_request_nested_router.register(prefix='stock_request_itemsvs', viewset=StockRequestItemViewSets,
                                     basename='stock_request_items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(stock_request_nested_router.urls)),
]
