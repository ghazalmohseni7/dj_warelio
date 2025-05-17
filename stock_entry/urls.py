from django.urls import path, include
from dj_warelio.routers import router
from stock_entry.views import StockEntryViewSets

router.register(prefix='stockentryvs', viewset=StockEntryViewSets, basename='stockentry')
urlpatterns = [path('', include(router.urls))]
