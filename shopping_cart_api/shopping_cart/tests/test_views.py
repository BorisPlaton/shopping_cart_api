import json

import pytest
from django.urls import reverse

from shopping_cart.models import ShoppingCart


@pytest.mark.django_db
class TestShoppingCartView:

    @pytest.fixture
    def serialized_ordered_product(self, create_product):
        return {'slug': create_product().slug, 'quantity': 2}

    def test_cookie_with_shopping_cart_id_is_created_when_post_request_is_sent(
            self, serialized_ordered_product, api_client
    ):
        response = api_client.post(
            reverse('shopping_cart:cart-list'), json.dumps(serialized_ordered_product),
            content_type='application/json'
        )
        assert response.cookies['cart_id'].value == str(ShoppingCart.objects.first().pk)

    def test_response_on_post_request_has_201_status_code_and_valid_data(
            self, serialized_ordered_product, api_client
    ):
        response = api_client.post(
            reverse('shopping_cart:cart-list'), json.dumps(serialized_ordered_product),
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data.keys() == {'slug', 'quantity'}

    def test_post_request_create_new_records_in_db(self, api_client, serialized_ordered_product):
        response = api_client.post(
            reverse('shopping_cart:cart-list'), json.dumps(serialized_ordered_product),
            content_type='application/json'
        )
        shopping_cart = ShoppingCart.objects.get(pk=response.cookies['cart_id'].value)
        ordered_product = shopping_cart.orders.get(product__slug=serialized_ordered_product['slug'])
        assert ordered_product.quantity == serialized_ordered_product['quantity']
