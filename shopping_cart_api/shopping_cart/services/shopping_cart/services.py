from django.core.exceptions import ValidationError

from shopping_cart.models import ShoppingCart
from shopping_cart.services.shopping_cart.cart_cookie_manager import CartCookieManager
from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_by_id


def get_or_create_shopping_cart_from_cookies(request_cookies: dict) -> ShoppingCart:
    """
    Returns a shopping cart from the cookies. If the cookie or the
    shopping cart doesn't exist, it will create a new one.
    """
    cart_cookie_manager = CartCookieManager(request_cookies)
    shopping_cart_id = cart_cookie_manager.get_shopping_cart_id()
    if not shopping_cart_id:
        return create_shopping_cart()
    try:
        return get_shopping_cart_by_id(shopping_cart_id)
    except (ShoppingCart.DoesNotExist, ValidationError):
        return create_shopping_cart()


def create_shopping_cart() -> ShoppingCart:
    """
    Creates and returns new shopping cart instance.
    """
    return ShoppingCart.objects.create()


def set_shopping_cart_id_cookie(response_cookies: dict, shopping_cart_id: str):
    """
    Sets a cookie with the cart id.
    """
    return CartCookieManager(response_cookies).set_shopping_cart_id(shopping_cart_id)
