import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound

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
