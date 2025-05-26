import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from faker import Faker
from product.models import Product
from warehouse.models import WareHouse
from inventory.models import Inventory
from stock_request.models import StockRequest, StockRequestItem

fake = Faker()


@pytest.mark.django_db
class TestPostSRI:
    def test_create_with_superuser_returns_201(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=5)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )
        sr = baker.make(StockRequest, warehouse=ses[0].warehouse, requested_by=manager)
        data = {
            'stock_request_id': sr.id,
            'product_id': ses[0].product.id,
            'quantity': 2
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/', data=data)
        # assert
        assert response.status_code == 201

    def test_create_with_staff_returns_201(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=5)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )
        sr = baker.make(StockRequest, warehouse=ses[0].warehouse, requested_by=manager)
        data = {
            'stock_request_id': sr.id,
            'product_id': ses[0].product.id,
            'quantity': 2
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/', data=data)
        # assert
        assert response.status_code == 201

    def test_create_with_normal_user_returns_403(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=5)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )
        sr = baker.make(StockRequest, warehouse=ses[0].warehouse, requested_by=manager)
        data = {
            'stock_request_id': sr.id,
            'product_id': ses[0].product.id,
            'quantity': 2
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/', data=data)
        # assert
        assert response.status_code == 403

    def test_create_with_bad_data_returns_400(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=5)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )
        sr = baker.make(StockRequest, warehouse=ses[0].warehouse, requested_by=manager)
        data = {
            'stock_request_id': 1111111,
            'product_id': 1111111,
            'quantity': 2
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post(f'/stock_requstvs/{sr.id}/stock_request_itemsvs/', data=data)
        # assert
        print("///////////", response.content)
        assert response.status_code == 400
