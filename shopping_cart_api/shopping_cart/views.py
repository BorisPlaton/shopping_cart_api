from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from view_mixins.mixins.compounds import CompoundMixin
from shopping_cart.serializers import (
    OrderedProductSerializer, ShoppingCartSerializer, SpecificOrderedProductSerializer
)
from shopping_cart.services.ordered_product.services import create_ordered_product
from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_from_cookies
from shopping_cart.services.shopping_cart.services import (
    get_or_create_shopping_cart_from_cookies,
    set_shopping_cart_id_cookie, update_products_quantity_in_cart, delete_products_from_shopping_cart
)


class ShoppingCartView(CompoundMixin, GenericViewSet):
    """
    The view for interaction with the user's shopping cart.
    """

    queryset = True
    serializer_class = {
        ('create', 'products_quantity'): OrderedProductSerializer,
        'delete_products': SpecificOrderedProductSerializer,
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
        validated_data = self.get_request_data(data=request.data)
        cart = get_or_create_shopping_cart_from_cookies(request.COOKIES)
        response = Response(
            self.get_serializer(create_ordered_product(cart, validated_data)).data,
            status=201
        )
        set_shopping_cart_id_cookie(response.cookies, cart)
        return response

    @action(methods=['patch'], detail=False, url_path='products/quantity')
    def products_quantity(self, request: Request):
        """
        Updates products quantity in cart. Products are found by their
        slug.
        """
        validated_data = self.get_request_data(data=request.data, many=True)
        altered_products = update_products_quantity_in_cart(
            get_shopping_cart_from_cookies(request.COOKIES),
            validated_data
        )
        return Response(self.get_serializer(altered_products, many=True).data)

    @action(methods=['patch'], detail=False, url_path='products')
    def delete_products(self, request: Request):
        """
        Deletes products from the shopping cart.
        """
        deleted_products_amount = delete_products_from_shopping_cart(
            get_shopping_cart_from_cookies(request.COOKIES),
            self.get_request_data(data=request.data, many=True)
        )
        return Response({'amount': deleted_products_amount})


class UserOrdersView(CompoundMixin, GenericViewSet):
    """
    The view class is responsible for user orders.
    """

    queryset = True
    serializer_class = {
        'create': ShoppingCartSerializer,
    }

    def create(self, request: Request):
        """
        Creates a new order for the not authenticated user. Additional
        credentials are required.
        """

    @action(methods=['post'], permission_classes=[IsAuthenticated], detail=True)
    def authenticated(self):
        """
        Creates a new order for the authenticated user. Contact
        information is retrieved from the user model.
        """
