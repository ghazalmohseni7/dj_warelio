import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from inventory.models import Inventory
from warehouse.models import WareHouse
from product.models import Product


@pytest.mark.django_db
class TestGetListInventory:
    def test_list_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)

        manager = baker.make(User)

        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)

        products = baker.make(Product, _quantity=5)

        inventories = []
        for i in range(10):
            inventories.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/inventoryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)

        manager = baker.make(User)

        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)

        products = baker.make(Product, _quantity=5)

        inventories = []
        for i in range(10):
            inventories.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/inventoryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)

        manager = baker.make(User)

        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)

        products = baker.make(Product, _quantity=5)

        inventories = []
        for i in range(10):
            inventories.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/inventoryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_empty_table_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/inventoryvs/')
        # assert
        assert response.status_code == 200


@pytest.mark.django_db
class TestGetDetailInventory:
    def test_detail_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        product = baker.make(Product)
        inventory = baker.make(Inventory, warehouse=warehouse, product=product)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/inventoryvs/{inventory.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        product = baker.make(Product)
        inventory = baker.make(Inventory, warehouse=warehouse, product=product)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/inventoryvs/{inventory.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        manager = baker.make(User)
        warehouse = baker.make(WareHouse, manager=manager)
        product = baker.make(Product)
        inventory = baker.make(Inventory, warehouse=warehouse, product=product)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/inventoryvs/{inventory.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_empty_table_returns_404(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/inventoryvs/1/')
        # assert
        assert response.status_code == 404


@pytest.mark.django_db
class TestGetSummaryItemsInventory:
    def test_si_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)

        manager = baker.make(User)

        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)

        products = baker.make(Product, _quantity=5)

        inventories = []
        for i in range(10):
            inventories.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/inventoryvs/summary_items/?product_id=1')
        # assert
        assert response.status_code == 200

    def test_si_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)

        manager = baker.make(User)

        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)

        products = baker.make(Product, _quantity=5)

        inventories = []
        for i in range(10):
            inventories.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/inventoryvs/summary_items/?warehouse_id=1')
        # assert
        assert response.status_code == 200

    def test_si_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)

        manager = baker.make(User)

        warehouses = baker.make(WareHouse, manager=manager, _quantity=2)

        products = baker.make(Product, _quantity=5)

        inventories = []
        for i in range(10):
            inventories.append(
                baker.make(Inventory, warehouse=warehouses[i % 2], product=products[i % 5])
            )

        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/inventoryvs/summary_items/?product_id=1&warehouse_id=1')
        # assert
        assert response.status_code == 200

    def test_si_with_empty_table_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/inventoryvs/summary_items/')
        # assert
        assert response.status_code == 200
