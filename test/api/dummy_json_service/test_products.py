import random

import pytest
from faker import Faker

from src.api.dummy_json_service.helpers.API_assertions import assert_pagination, assert_unique_field
from src.api.dummy_json_service.helpers.API_utils import get_random_id
from src.api.dummy_json_service.models.common_models import BasicErrorResponse
from src.api.dummy_json_service.models.product_models import ProductResponse, ProductListResponse, \
    DeletedProductResponse


@pytest.mark.api
def test_get_all_products(dummy_api_client):
    response = dummy_api_client.get('products')

    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())
    assert len(products_response.products) > 0, 'There should be at least one product'
    assert_pagination(products_response)
    assert_unique_field(products_response.products, 'id')


@pytest.mark.api
def test_products_paginating(dummy_api_client):
    limit = 10

    #First 10 products
    response = dummy_api_client.get('products', params={'limit': limit, 'skip': 0})

    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())
    assert len(products_response.products) <= limit, f'There should be {limit} products at page or less'
    assert_pagination(products_response, requested_limit=limit)
    assert_unique_field(products_response.products, 'id')

    total_products_number = products_response.total

    #Second 10 products
    response = dummy_api_client.get('products', params={'limit': limit, 'skip': limit})

    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())
    assert len(products_response.products) <= limit, f'There should be {limit} products at page or less'
    assert_pagination(products_response, requested_limit=limit, requested_skip=limit,
                      expected_total=total_products_number)
    assert_unique_field(products_response.products, 'id')

    #Last 10 products
    skip = total_products_number - limit

    response = dummy_api_client.get('products', params={'limit': limit, 'skip': skip})

    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())

    assert len(products_response.products) == limit, f'There should be {limit} products at page'
    assert_pagination(products_response, requested_limit=limit, requested_skip=skip,
                      expected_total=total_products_number)
    assert_unique_field(products_response.products, 'id')


@pytest.mark.api
def test_get_product_by_id(dummy_api_client):
    product_id = get_random_id()

    response = dummy_api_client.get(f'products/{product_id}')

    assert response.status_code == 200
    products_response = ProductResponse.model_validate(response.json())
    assert products_response.id == product_id


@pytest.mark.api
def test_get_product_by_invalid_id(dummy_api_client):
    product_id = get_random_id(start=100000, end=200000)

    response = dummy_api_client.get(f'products/{product_id}')

    assert response.status_code == 404
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.message == f"Product with id '{product_id}' not found"


@pytest.mark.api
@pytest.mark.parametrize('search_word', ['phone', 'laptop', 'milk'])
def test_search_products(dummy_api_client, search_word):
    response = dummy_api_client.get('products/search', params={'q': search_word})

    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())
    assert len(products_response.products) > 0, 'There should be at least one product'
    assert_pagination(products_response)
    assert_unique_field(products_response.products, 'id')
    for product in products_response.products:
        assert (search_word in product.title.lower()) or (search_word in product.description.lower())


@pytest.mark.api
def test_search_products_invalid_query(dummy_api_client):
    search_word = 'eqwdadasdas'

    response = dummy_api_client.get('products/search', params={'q': search_word})

    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())
    assert len(products_response.products) == 0, f'There should be no products for query {search_word}'
    assert_pagination(products_response, expected_total=0)


@pytest.mark.api
def test_get_products_by_category_with_limit(dummy_api_client):
    response = dummy_api_client.get('products/category-list')

    assert response.status_code == 200
    category_response = response.json()
    assert len(category_response) > 0, 'There should be at least one category'

    categories = random.sample(category_response, 3)
    for category in categories:
        limit = 5
        response = dummy_api_client.get(f'products/category/{category}', params={'limit': limit})

        assert response.status_code == 200
        products_response = ProductListResponse.model_validate(response.json())
        assert len(products_response.products) > 0, 'There should be at least one product'
        assert_pagination(products_response, requested_limit=limit)
        assert_unique_field(products_response.products, 'id')
        for product in products_response.products:
            assert category == product.category


@pytest.mark.api
@pytest.mark.xfail(reason="DummyJSON returns mocked partial response")
def test_update_product_title(dummy_api_client):
    product_id = get_random_id()
    new_title = Faker().word()

    response = dummy_api_client.put(f'products/{product_id}', payload={'title': new_title})

    assert response.status_code == 200
    product_response = ProductResponse.model_validate(response.json())
    assert product_response.title == new_title


@pytest.mark.api
def test_delete_product(dummy_api_client):
    product_id = get_random_id()

    response = dummy_api_client.delete(f'products/{product_id}')

    assert response.status_code == 200
    product_response = DeletedProductResponse.model_validate(response.json())
    assert product_response.isDeleted
