import random

from config import settings
from src.api.dummy_json_service.models.auth_models import AuthRequest
from src.api.dummy_json_service.models.cart_models import CartUpdateProduct, CartUpdateRequest


def get_valid_user(expiresInMins=None, **kwargs):
    user = {'username': settings.DUMMY_TEST_API_USERNAME, 'password': settings.DUMMY_TEST_API_PASSWORD}
    user.update(kwargs)
    if expiresInMins is not None:
        user.update({'expiresInMins': expiresInMins})
    return AuthRequest(**user)

def get_random_id(start = 1, end = 100):
    return random.randint(start, end)

def get_product_for_cart():
    return CartUpdateProduct(id=get_random_id(),
                quantity = random.randint(1, 100))

def get_cart_payload(user_id = None, merge = None, number_of_products = 1):
    payload = dict(products = [])
    for _ in range(number_of_products):
        payload['products'].append(get_product_for_cart().model_dump())
    if user_id:
        payload['user_id'] = user_id
    if merge:
        payload['merge'] = merge

    return CartUpdateRequest(**payload)
