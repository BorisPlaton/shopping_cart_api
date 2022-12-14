import pytest
from model_bakery import baker

from shopping_cart.models import ShoppingCart
from shopping_cart.services.cookies.services import (
    get_or_create_shopping_cart_from_cookies,
    set_shopping_cart_id_cookie
)


@pytest.mark.django_db
class TestOrdersServices:

    def test_get_or_create_shopping_cart_from_cookies_returns_shopping_cart_from_cookie(self):
        shopping_cart = baker.make(ShoppingCart)
        request_cookies = {'cart_id': str(shopping_cart.pk)}
        assert get_or_create_shopping_cart_from_cookies(request_cookies) == shopping_cart

    def test_get_or_create_shopping_cart_from_cookies_creates_if_cart_id_is_wrong(self):
        request_cookies = {'cart_id': 'wrong-id'}
        shopping_cart = get_or_create_shopping_cart_from_cookies(request_cookies)
        assert isinstance(shopping_cart, ShoppingCart)
        assert request_cookies['cart_id'] != str(shopping_cart.pk)

    def test_set_shopping_cart_id_cookie_updates_cookies_dict(self):
        cookies = {}
        cart = baker.make(ShoppingCart)
        set_shopping_cart_id_cookie(cart, cookies)
        assert cookies['cart_id'] == str(cart.pk)
