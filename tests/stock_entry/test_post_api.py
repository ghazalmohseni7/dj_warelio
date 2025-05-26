import pytest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from model_bakery import baker
from faker import Faker
from stock_entry.models import StockEntry
from inventory.models import Inventory
from warehouse.models import WareHouse
from product.models import Product

fake = Faker()


@pytest.mark.django_db
class TestPostSE:
    def test_post_with_superuser_returns_201(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )
        inventory = get_object_or_404(Inventory, warehouse=warehouses[0], product=products[0])
        old_inventory_quantity = inventory.quantity
        data = {
            "quantity": 2,
            "warehouse_id": warehouses[0].id,
            "product_id": products[0].id,
            "received_by_id": manager.id
        }

        api_client.force_authenticate(user=user)
        # act
        response = api_client.post('/stockentryvs/', data=data)
        inventory.refresh_from_db()
        # assert
        assert response.status_code == 201
        assert inventory.quantity == old_inventory_quantity + data['quantity']

    def test_post_with_staff_returns_201(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)
        products = baker.make(Product, _quantity=5)
        ses = []
        for i in range(10):
            ses.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )
        inventory = get_object_or_404(Inventory, warehouse=warehouses[0], product=products[0])
        old_inventory_quantity = inventory.quantity
        data = {
            "quantity": 2,
            "warehouse_id": warehouses[0].id,
            "product_id": products[0].id,
            "received_by_id": manager.id
        }

        api_client.force_authenticate(user=user)
        # act
        response = api_client.post('/stockentryvs/', data=data)
        inventory.refresh_from_db()
        # assert
        assert response.status_code == 201
        assert inventory.quantity == old_inventory_quantity + data['quantity']

    def test_post_with_normal_user_returns_403(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        api_client.force_authenticate(user=user)
        # act
        response = response = api_client.post('/stockentryvs/', data={})
        # assert
        assert response.status_code == 403
