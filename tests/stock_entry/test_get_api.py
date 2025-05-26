import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from stock_entry.models import StockEntry
from warehouse.models import WareHouse
from product.models import Product


@pytest.mark.django_db
class TestGetListSE:
    def test_list_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(StockEntry, warehouse=warehouses[i % 2], product=products[i % 5], received_by=manager)
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/stockentryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(StockEntry, warehouse=warehouses[i % 2], product=products[i % 5], received_by=manager)
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/stockentryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(StockEntry, warehouse=warehouses[i % 2], product=products[i % 5], received_by=manager)
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/stockentryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_empty_table_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/stockentryvs/')
        # assert
        assert response.status_code == 200


@pytest.mark.django_db
class TestGetDetailSE:
    def test_detail_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        product = baker.make(Product)
        se = baker.make(StockEntry, warehouse=warehouse, product=product, received_by=manager)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stockentryvs/{se.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        product = baker.make(Product)
        se = baker.make(StockEntry, warehouse=warehouse, product=product, received_by=manager)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stockentryvs/{se.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        product = baker.make(Product)
        se = baker.make(StockEntry, warehouse=warehouse, product=product, received_by=manager)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/stockentryvs/{se.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_empty_table_returns_404(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/stockentryvs/1/')
        # assert
        assert response.status_code == 404
