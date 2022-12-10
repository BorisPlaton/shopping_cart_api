import pytest
from model_bakery import baker

from shopping_cart.models import ShoppingCart
from shopping_cart.services.shopping_cart.services import (
    create_shopping_cart, get_or_create_shopping_cart_from_cookies, set_shopping_cart_id_cookie
)


@pytest.mark.django_db
class TestShoppingCartServices:

    def test_create_shopping_cart_creates_new_record(self):
        shopping_cart = create_shopping_cart()
        assert isinstance(shopping_cart, ShoppingCart)

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
        cart_id = 'some id'
        set_shopping_cart_id_cookie(cookies, cart_id)
        assert cookies['cart_id'] == cart_id
