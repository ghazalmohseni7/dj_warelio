import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from faker import Faker
from category.models import Category

fake = Faker()


@pytest.mark.django_db
class TestUpdateCategory:
    def test_update_with_superuser_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        category = baker.make(Category)
        data = {
            'name': fake.name(),
            'description': fake.word()
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.patch(f'/categoryvs/{category.id}/', data=data)
        # assert
        assert response.status_code == 200

    def test_update_with_staff_returns_200(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        category = baker.make(Category)
        data = {
            'name': fake.name(),
            'description': fake.word()
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.patch(f'/categoryvs/{category.id}/', data=data)
        # assert
        assert response.status_code == 200

    def test_update_with_normal_user_returns_403(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        category = baker.make(Category)
        data = {
            'name': fake.name(),
            'description': fake.word()
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.patch(f'/categoryvs/{category.id}/', data=data)
        # assert
        assert response.status_code == 403

    def test_update_with_repeated_data_returns_400(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        category = baker.make(Category)
        category_ = baker.make(Category)
        data = {
            'name': category_.name,
            'description': "aaaaaaaaaaaaa"
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.patch(f'/categoryvs/{category.id}/', data=data)
        # assert
        assert response.status_code == 400

    def test_update_with_bad_data_returns_400(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        category = baker.make(Category)
        data = {
            'name': "1" * 1000000,
            'description': "aaaaaaaaaaaaa"
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.patch(f'/categoryvs/{category.id}/', data=data)
        # assert
        assert response.status_code == 400
