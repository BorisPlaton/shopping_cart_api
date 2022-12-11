from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from multiple_serializers.mixin import MultipleSerializerMixin
from shopping_cart.serializers import OrderedProductSerializer, ShoppingCartSerializer
from shopping_cart.services.ordered_product.services import create_ordered_product
from shopping_cart.services.shopping_cart.selectors import get_all_shopping_carts, get_shopping_cart_from_cookies
from shopping_cart.services.shopping_cart.services import (
    get_or_create_shopping_cart_from_cookies,
    set_shopping_cart_id_cookie
)


class ShoppingCartView(MultipleSerializerMixin, GenericViewSet):
    """
    The view for interaction with the user's shopping cart.
    """

    queryset = get_all_shopping_carts()
    serializer_class = {
        'create': OrderedProductSerializer,
        'list': ShoppingCartSerializer,
    }

    def list(self, request: Request):
        """
        Returns information about shopping cart.
        """
        return Response(
            self.get_serializer(get_shopping_cart_from_cookies(request.COOKIES), eager_loading=True).data
        )

    def create(self, request: Request):
        """
        Adds product to the shopping cart. If the cart doesn't already
        exist, it will be created.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = get_or_create_shopping_cart_from_cookies(request.COOKIES)
        response = Response(
            self.get_serializer(create_ordered_product(cart, serializer.validated_data)).data,
            status=201
        )
        set_shopping_cart_id_cookie(response.cookies, cart)
        return response
