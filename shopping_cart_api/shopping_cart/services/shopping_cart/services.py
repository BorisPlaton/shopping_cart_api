from django.core.exceptions import ValidationError

from shopping_cart.models import ShoppingCart
from shopping_cart.services.ordered_product.services import create_ordered_products
from shopping_cart.services.shopping_cart.cart_cookie_manager import CartCookieManager
from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_by_id


def add_products_to_cart_from_request(products: list[dict], request_cookies: dict):
    """
    Adds products to the user's shopping cart.
    """
    shopping_cart = get_or_create_shopping_cart_from_cookies(request_cookies)
    return create_ordered_products(shopping_cart, products)


def get_or_create_shopping_cart_from_cookies(request_cookies: dict) -> ShoppingCart:
    """
    Returns a shopping cart from the cookies. If the cookie or the
    shopping cart doesn't exist, it will create a new one and
    will set its id in the request cookies.
    """
    cart_cookie_manager = CartCookieManager(request_cookies)
    shopping_cart_id = cart_cookie_manager.get_shopping_cart_id()
    if not shopping_cart_id:
        return create_shopping_cart_and_set_cookies(request_cookies)
    try:
        return get_shopping_cart_by_id(shopping_cart_id)
    except (ShoppingCart.DoesNotExist, ValidationError):
        return create_shopping_cart_and_set_cookies(request_cookies)


def create_shopping_cart_and_set_cookies(request_cookies: dict) -> ShoppingCart:
    """
    Creates a new shopping cart and sets its id in the request cookies.
    """
    cart_cookie_manager = CartCookieManager(request_cookies)
    shopping_cart = create_shopping_cart()
    cart_cookie_manager.set_shopping_cart_id(str(shopping_cart.pk))
    return shopping_cart


def create_shopping_cart() -> ShoppingCart:
    """
    Creates and returns new shopping cart instance.
    """
    return ShoppingCart.objects.create()
