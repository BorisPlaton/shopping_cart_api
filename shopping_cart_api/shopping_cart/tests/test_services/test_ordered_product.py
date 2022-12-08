import pytest
from model_bakery import baker

from products.models import Product
from shopping_cart.models import ShoppingCart, OrderedProduct
from shopping_cart.services.ordered_product.services import create_ordered_products


@pytest.mark.django_db
class TestOrderedProductServices:

    def test_create_ordered_products_only_for_existing_products(self):
        assert not Product.objects.all()
        create_ordered_products(baker.make(ShoppingCart), [{'product_id': 1, 'quantity': 12}])
        assert not OrderedProduct.objects.all()

    def test_if_product_exists_ordered_product_will_be_created(self, create_product):
        product = create_product()
        create_products = create_ordered_products(
            baker.make(ShoppingCart), [{'product_id': product.pk, 'quantity': 12}]
        )
        assert OrderedProduct.objects.first() == create_products[0]
