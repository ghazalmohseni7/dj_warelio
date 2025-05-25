import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from category.models import Category


@pytest.mark.django_db
class TestGetListCategory:
    def test_list_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        baker.make(Category, _quantity=10)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/categoryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        baker.make(Category, _quantity=10)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/categoryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        baker.make(Category, _quantity=10)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/categoryvs/')
        # assert
        assert response.status_code == 200

    def test_list_with_empty_table_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/categoryvs/')
        # assert
        assert response.status_code == 200


@pytest.mark.django_db
class TestGetDetailCategory:
    def test_detail_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        category = baker.make(Category)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/categoryvs/{category.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        category = baker.make(Category)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/categoryvs/{category.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_normal_user_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        category = baker.make(Category)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get(f'/categoryvs/{category.id}/')
        # assert
        assert response.status_code == 200

    def test_detail_with_empty_table_returns_404(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.get('/categoryvs/1/')
        # assert
        assert response.status_code == 404
