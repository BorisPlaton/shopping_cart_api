import pytest
from model_bakery import baker
from rest_framework.exceptions import ValidationError

from shopping_cart.models import OrderedProduct
from shopping_cart.serializer import OrderedProductSerializer


@pytest.mark.django_db
class TestOrderedProductSerializer:

    def test_ordered_product_is_deserialized_with_id_field(self):
        ordered_product_data = {'product_id': 1, 'quantity': 2}
        assert OrderedProductSerializer(data=ordered_product_data).is_valid()

    @pytest.mark.parametrize(
        'ordered_product_data',
        [
            {'quantity': 1},
            {'product_id': 1},
            {'product_id': -1, 'quantity': 2},
            {'product_id': 1, 'quantity': 0},
            {'product_id': 1, 'quantity': -1},
            {},
        ]
    )
    def test_ordered_product_serializer_invalid_data_cases(self, ordered_product_data):
        with pytest.raises(ValidationError):
            OrderedProductSerializer(data=ordered_product_data).is_valid(raise_exception=True)

    def test_serialization_fetch_related_product_id(self, create_product):
        ordered_product = baker.make(OrderedProduct, quantity=2, product=create_product())
        serializer_data = OrderedProductSerializer(ordered_product).data
        assert serializer_data.keys() == {'product_id', 'quantity'}
        assert serializer_data['product_id'] == ordered_product.product.pk
