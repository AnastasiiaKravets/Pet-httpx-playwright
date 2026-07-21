import pytest

from src.api.dummy_json_service.helpers.assertions import assert_pagination, assert_unique_field, \
    assert_products_in_cart
from src.api.dummy_json_service.helpers.data_helper import get_random_id, get_cart_payload
from src.api.dummy_json_service.models.cart_models import CartListResponse, CartResponse, DeletedCartResponse
from src.api.dummy_json_service.models.common_models import BasicErrorResponse


@pytest.mark.api
def test_get_all_carts(dummy_api_client):
    response = dummy_api_client.get('carts')
    assert response.status_code == 200

    carts_response = CartListResponse.model_validate(response.json())

    assert len(carts_response.carts) > 0, 'There should be at least one cart'
    assert_pagination(carts_response)
    assert_unique_field(carts_response.carts, 'id')


@pytest.mark.api
def test_get_cart_by_id(dummy_api_client):
    cart_id = get_random_id()

    response = dummy_api_client.get(f'carts/{cart_id}')

    assert response.status_code == 200
    carts_response = CartResponse.model_validate(response.json())
    assert carts_response.id == cart_id


@pytest.mark.api
def test_get_cart_by_invalid_id(dummy_api_client):
    cart_id = get_random_id(start=100000, end=200000)

    response = dummy_api_client.get(f'carts/{cart_id}')

    assert response.status_code == 404
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.message == f"Cart with id '{cart_id}' not found"


@pytest.mark.api
def test_get_carts_by_user_id(dummy_api_client):
    user_id = get_random_id()

    response = dummy_api_client.get(f'carts/user/{user_id}')

    assert response.status_code == 200
    carts_response = CartListResponse.model_validate(response.json())
    assert len(carts_response.carts) > 0, 'There should be at least one cart'
    assert_pagination(carts_response)
    assert_unique_field(carts_response.carts, 'id')


@pytest.mark.api
def test_create_cart(dummy_api_client):
    cart_payload = get_cart_payload(user_id = get_random_id(), number_of_products=3)

    response = dummy_api_client.post(f'carts/add', payload=cart_payload)

    assert response.status_code == 201
    cart_response = CartResponse.model_validate(response.json())
    assert cart_response.user_id == cart_payload.user_id
    assert_products_in_cart(cart_payload, cart_response, exact_match=True)


@pytest.mark.api
def test_update_cart(dummy_api_client):
    cart_id = get_random_id()
    cart_payload = get_cart_payload(merge=True, number_of_products=2)

    response = dummy_api_client.put(f'carts/{cart_id}', payload=cart_payload)
    assert response.status_code == 200
    cart_response = CartResponse.model_validate(response.json())
    assert_products_in_cart(cart_payload, cart_response)


@pytest.mark.api
def test_delete_cart(dummy_api_client):
    cart_id = get_random_id()

    response = dummy_api_client.delete(f'carts/{cart_id}')

    assert response.status_code == 200
    cart_response = DeletedCartResponse.model_validate(response.json())
    assert cart_response.isDeleted
