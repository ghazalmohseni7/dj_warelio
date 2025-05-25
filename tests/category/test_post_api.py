import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from faker import Faker
from category.models import Category

fake = Faker()


@pytest.mark.django_db
class TestPostCategory:
    def test_create_with_superuser_returns_201(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        category = {
            'name': fake.name(),
            'description': fake.word()
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post('/categoryvs/', data=category)
        # assert
        assert response.status_code == 201

    def test_create_with_staff_returns_201(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        category = {
            'name': fake.name(),
            'description': fake.word()
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post('/categoryvs/', data=category)
        # assert
        assert response.status_code == 201

    def test_create_with_normal_user_returns_403(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        category = {
            'name': fake.name(),
            'description': fake.word()
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post('/categoryvs/', data=category)
        # assert
        assert response.status_code == 403

    def test_create_with_repeated_data_returns_400(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        category = baker.make(Category)
        data = {
            'name': category.name,
            'description': "aaaaaaaaaaaaa"
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post('/categoryvs/', data=data)
        # assert
        assert response.status_code == 400

    def test_create_with_bad_data_returns_400(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)

        data = {
            'name': "1" * 1000000,
            'description': "aaaaaaaaaaaaa"
        }
        api_client.force_authenticate(user=user)
        # act
        response = api_client.post('/categoryvs/', data=data)
        # assert
        assert response.status_code == 400
