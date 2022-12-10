import json

import pytest
from django.urls import reverse

from shopping_cart.models import ShoppingCart


@pytest.mark.django_db
class TestShoppingCartView:

    @pytest.fixture
    def serialized_ordered_products(self, create_product):
        return [
            {'product_id': product.pk, 'quantity': 2} for product in [create_product() for _ in range(3)]
        ]

    def test_cookie_with_shopping_cart_id_is_created_when_post_request_is_sent(
            self, serialized_ordered_products, api_client
    ):
        response = api_client.post(
            reverse('shopping_cart:cart-list'), json.dumps(serialized_ordered_products),
            content_type='application/json'
        )
        assert response.cookies['cart_id'].value == str(ShoppingCart.objects.first().pk)

    def test_response_on_post_request_has_201_status_code_and_valid_data(
            self, serialized_ordered_products, api_client
    ):
        response = api_client.post(
            reverse('shopping_cart:cart-list'), json.dumps(serialized_ordered_products),
            content_type='application/json'
        )
        assert response.status_code == 201
        for data in response.data:
            assert data.keys() == {'product_id', 'quantity'}
