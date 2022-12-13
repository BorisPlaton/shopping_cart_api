from rest_framework.permissions import BasePermission

from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_id_from_cookies


class HasCartIdCookie(BasePermission):
    """
    Base check if the cart id cookie exists.
    """

    def has_permission(self, request, view):
        cart_id = get_shopping_cart_id_from_cookies(request.COOKIES)
        return bool(cart_id)
