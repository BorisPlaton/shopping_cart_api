import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound

from exceptions.http_exceptions import StateConflict
from products.models import Product
from shopping_cart.models import ShoppingCart, OrderedProduct
from shopping_cart.services.ordered_product.services import create_ordered_product


@pytest.mark.django_db
class TestOrderedProductServices:

    def test_create_ordered_product_only_for_existing_products(self):
        assert not Product.objects.all()
        with pytest.raises(NotFound):
            create_ordered_product(baker.make(ShoppingCart), {'slug': 'some-slug', 'quantity': 12})
        assert not OrderedProduct.objects.all()

    def test_if_product_exists_ordered_product_will_be_created(self, create_product):
        product = create_product()
        created_product = create_ordered_product(
            baker.make(ShoppingCart), {'slug': product.slug, 'quantity': 12}
        )
        assert OrderedProduct.objects.first() == created_product

    def test_if_product_is_already_in_cart_exception_is_raised(self, create_product):
        product = create_product()
        cart = baker.make(ShoppingCart)
        create_ordered_product(cart, {'slug': product.slug, 'quantity': 12})
        with pytest.raises(StateConflict):
            create_ordered_product(cart, {'slug': product.slug, 'quantity': 2})
