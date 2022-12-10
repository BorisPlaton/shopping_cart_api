from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from multiple_serializers.mixin import MultipleSerializerMixin
from shopping_cart.serializer import OrderedProductSerializer
from shopping_cart.services.ordered_product.services import create_ordered_products
from shopping_cart.services.shopping_cart.services import get_or_create_shopping_cart_from_cookies, \
    set_shopping_cart_id_cookie


class ShoppingCartView(MultipleSerializerMixin, GenericViewSet):
    """
    The view for interaction with the user's shopping cart.
    """

    serializer_class = {
        'create': OrderedProductSerializer,
    }

    def list(self, request: Request):
        """
        Retrieves information about shopping cart.
        """

    def create(self, request: Request):
        """
        Adds products to the shopping cart. If the cart doesn't already
        exist, it will be created.
        """
        serializer: OrderedProductSerializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        cart = get_or_create_shopping_cart_from_cookies(request.COOKIES)
        response = Response(
            self.get_serializer(create_ordered_products(cart, serializer.validated_data), many=True).data,
            status=201
        )
        set_shopping_cart_id_cookie(response.cookies, str(cart.pk))
        return response
