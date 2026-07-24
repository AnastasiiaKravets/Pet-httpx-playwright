from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel
from src.api.dummy_json_service.models.common_models import PaginatedStrictModel


def assert_pagination(model: PaginatedStrictModel, requested_limit=30, requested_skip=0, expected_total = None):
    #if total count is less than requested limit endpoint returns total count and limit with the same data
    expected_limit = max(min(requested_limit, model.total - requested_skip), 0)

    assert model.skip == requested_skip
    assert model.limit == expected_limit
    if expected_total is not None:
        assert model.total == expected_total, (f'Expected total count of items are different from actual, '
                                               f'exected {expected_total}, actual {model.total}')
    else:
        assert model.total > 0, 'There should be at least one item'


def assert_unique_field(items: Iterable[Any], field: str) -> None:
    seen = set()
    duplicates = set()

    for item in items:
        value = getattr(item, field)

        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)

    assert not duplicates, (f"Duplicate values found in '{field}': {duplicates}")


def assert_products_in_cart(payload_products: BaseModel, response_products: BaseModel, exact_match=False):
    expected = {(product.id, product.quantity) for product in payload_products.products}
    actual = {(product.id, product.quantity) for product in response_products.products}

    if exact_match:
        assert expected == actual, (f'Different products id or quantity. \n'
                                    f'Expected (id, quantity):{expected}, \n'
                                    f'Actual (id, quantity):  {actual}')
    else:
        assert expected.issubset(actual), (f'Different products id or quantity. \n'
                                           f'Expected (id, quantity):{expected}, \n'
                                           f'Actual (id, quantity):  {actual}')
