import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from category.models import Category


@pytest.mark.django_db
class TestDeleteCategory:
    def test_delete_with_superuser_returns_204(self, api_client):
        # arrange
        user = baker.make(User, is_superuser=True)
        category = baker.make(Category)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.delete(f'/categoryvs/{category.id}/')
        # assert
        assert response.status_code == 204

    def test_delete_with_staff_returns_204(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        category = baker.make(Category)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.delete(f'/categoryvs/{category.id}/')
        # assert
        assert response.status_code == 204

    def test_delete_with_normal_user_returns_403(self, api_client):
        # arrange
        user = baker.make(User, is_active=True)
        category = baker.make(Category)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.delete(f'/categoryvs/{category.id}/')
        # assert
        assert response.status_code == 403

    def test_delete_with_empty_table_returns_404(self, api_client):
        # arrange
        user = baker.make(User, is_staff=True)
        api_client.force_authenticate(user=user)
        # act
        response = api_client.delete('/categoryvs/1/')
        # assert
        assert response.status_code == 404
