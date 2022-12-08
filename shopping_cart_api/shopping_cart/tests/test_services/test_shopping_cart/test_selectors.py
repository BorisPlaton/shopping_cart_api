import pytest
from model_bakery import baker

from shopping_cart.models import ShoppingCart
from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_by_id


@pytest.mark.django_db
class TestShoppingCartSelectors:

    def test_get_shopping_cart_by_id_returns_specific_product(self):
        shopping_cart = baker.make(ShoppingCart)
        baker.make(ShoppingCart)
        assert get_shopping_cart_by_id(shopping_cart.pk) == shopping_cart
