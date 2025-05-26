import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from product.models import Product
from warehouse.models import WareHouse
from stock_request.models import StockRequest, StockRequestItem


@pytest.mark.django_db
class TestGetListSRI:
    def test_list_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        products = baker.make(Product, _quantity=5)
        sr = baker.make(StockRequest, warehouse=warehouse, requested_by=manager)
        sris = []
        for i in range(10):
            sris.append(
                baker.make(StockRequestItem, stock_request=sr, product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        products = baker.make(Product, _quantity=5)
        sr = baker.make(StockRequest, warehouse=warehouse, requested_by=manager)
        sris = []
        for i in range(10):
            sris.append(
                baker.make(StockRequestItem, stock_request=sr, product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        products = baker.make(Product, _quantity=5)
        sr = baker.make(StockRequest, warehouse=warehouse, requested_by=manager)
        sris = []
        for i in range(10):
            sris.append(
                baker.make(StockRequestItem, stock_request=sr, product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_empty_table_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        sr = baker.make(StockRequest, warehouse=warehouse, requested_by=manager)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/')
        # assert
        assert response.status_code == 200


@pytest.mark.django_db
class TestGetDetailSRI:
    def test_detail_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        products = baker.make(Product, _quantity=5)
        sr = baker.make(StockRequest, warehouse=warehouse, requested_by=manager)
        sris = []
        for i in range(10):
            sris.append(
                baker.make(StockRequestItem, stock_request=sr, product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/{sris[0].id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        products = baker.make(Product, _quantity=5)
        sr = baker.make(StockRequest, warehouse=warehouse, requested_by=manager)
        sris = []
        for i in range(10):
            sris.append(
                baker.make(StockRequestItem, stock_request=sr, product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/{sris[0].id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        products = baker.make(Product, _quantity=5)
        sr = baker.make(StockRequest, warehouse=warehouse, requested_by=manager)
        sris = []
        for i in range(10):
            sris.append(
                baker.make(StockRequestItem, stock_request=sr, product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/{sris[0].id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_empty_table_returns_404(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        sr = baker.make(StockRequest, warehouse=warehouse, requested_by=manager)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/1/')
        # assert
        assert response.status_code == 404
