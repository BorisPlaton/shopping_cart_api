import pytest
from model_bakery import baker

from shopping_cart.models import ShoppingCart
from shopping_cart.services.shopping_cart.services import (
    create_shopping_cart, create_shopping_cart_and_set_cookies,
    get_or_create_shopping_cart_from_cookies
)


@pytest.mark.django_db
class TestShoppingCartServices:

    def test_create_shopping_cart_creates_new_record(self):
        shopping_cart = create_shopping_cart()
        assert isinstance(shopping_cart, ShoppingCart)

    def test_create_shopping_cart_and_set_cookies_updates_cookies(self):
        request_cookies = {'some_cookie': 'value'}
        created_shopping_cart = create_shopping_cart_and_set_cookies(request_cookies)
        assert isinstance(created_shopping_cart, ShoppingCart)
        assert request_cookies.keys() == {'some_cookie', 'cart_id'}
        assert request_cookies['cart_id'] == str(created_shopping_cart.pk)

    def test_get_or_create_shopping_cart_from_cookies_updates_cookies_and_creates_new_shopping_cart(self):
        assert not ShoppingCart.objects.all()
        request_cookies = {}
        new_cart = get_or_create_shopping_cart_from_cookies(request_cookies)
        assert request_cookies['cart_id'] == str(new_cart.pk)

    def test_get_or_create_shopping_cart_from_cookies_create_shopping_cart_from_cookie(self):
        shopping_cart = baker.make(ShoppingCart)
        request_cookies = {'cart_id': str(shopping_cart.pk)}
        assert get_or_create_shopping_cart_from_cookies(request_cookies) == shopping_cart

    def test_get_or_create_shopping_cart_create_and_updates_cookies_if_cart_id_is_wrong(self):
        request_cookies = {'cart_id': 'wrong-id'}
        shopping_cart = get_or_create_shopping_cart_from_cookies(request_cookies)
        assert isinstance(shopping_cart, ShoppingCart)
        assert request_cookies['cart_id'] == str(shopping_cart.pk)
