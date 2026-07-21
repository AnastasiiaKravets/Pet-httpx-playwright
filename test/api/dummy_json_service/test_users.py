import pytest
from faker import Faker

from src.api.dummy_json_service.helpers.API_assertions import assert_pagination, assert_unique_field
from src.api.dummy_json_service.helpers.API_utils import get_random_id
from src.api.dummy_json_service.models.cart_models import CartListResponse
from src.api.dummy_json_service.models.user_models import UserResponse, UserListResponse, DeletedUserResponse


@pytest.mark.api
def test_get_all_users(dummy_api_client):
    response = dummy_api_client.get('users')

    assert response.status_code == 200
    user_response = UserListResponse.model_validate(response.json())
    assert len(user_response.users) > 0, 'There should be at least one user'
    assert_pagination(user_response)
    assert_unique_field(user_response.users, 'id')
    assert_unique_field(user_response.users, 'email')


@pytest.mark.api
def test_get_user_by_id(dummy_api_client):
    user_id = get_random_id()

    response = dummy_api_client.get(f'user/{user_id}')

    assert response.status_code == 200
    user_response = UserResponse.model_validate(response.json())
    assert user_response.id == user_id


@pytest.mark.api
def test_update_user_data(dummy_api_client):
    # Not interesting as there is no field validation logic at the endpoint
    user_id = get_random_id()
    new_name = Faker().name()

    response = dummy_api_client.put(f'user/{user_id}',
                                    payload={'firstName': new_name})

    assert response.status_code == 200
    user_response = UserResponse.model_validate(response.json())
    assert user_response.first_name == new_name


@pytest.mark.api
def test_delete_user(dummy_api_client):
    user_id = get_random_id()

    response = dummy_api_client.delete(f'user/{user_id}')

    assert response.status_code == 200
    user_response = DeletedUserResponse.model_validate(response.json())
    assert user_response.isDeleted


@pytest.mark.api
def test_get_user_carts_by_user_id(dummy_api_client):
    user_id = get_random_id()

    response = dummy_api_client.get(f'user/{user_id}/carts')

    assert response.status_code == 200
    carts_response = CartListResponse.model_validate(response.json())
    assert len(carts_response.carts) > 0, 'There should be at least one cart'
    assert_pagination(carts_response)
    assert_unique_field(carts_response.carts, 'id')
