from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound, ValidationError as RestValidationError

from shopping_cart.models import ShoppingCart
from shopping_cart.services.shopping_cart.cart_cookie_manager import CartCookieManager


def get_shopping_cart_from_cookies(request_cookies: dict):
    """
    Returns shopping cart from cookies. If the cookie doesn't exist or
    cart id is wrong then the exception is raised.
    """
    shopping_cart_id = get_shopping_cart_id_from_cookies(request_cookies)
    if not shopping_cart_id:
        raise NotFound("You don't have a shopping cart.")
    return get_shopping_cart_by_id(shopping_cart_id)


def get_shopping_cart_id_from_cookies(request_cookies: dict):
    """
    Returns shopping cart id from request cookies. If none, returns
    None.
    """
    cart_cookie_manager = CartCookieManager(request_cookies)
    return cart_cookie_manager.get_shopping_cart_id()


def get_shopping_cart_by_id(shopping_cart_id: str):
    """
    Returns the shopping cart by its id. If none, raises exception.
    """
    try:
        return ShoppingCart.objects.get(pk=shopping_cart_id)
    except ShoppingCart.DoesNotExist:
        raise NotFound("Shopping cart with id %s doesn't exist." % shopping_cart_id)
    except (ValidationError, ValueError):
        raise RestValidationError("Your cookie with cart id %s is invalid" % shopping_cart_id)


def get_all_shopping_carts() -> QuerySet[ShoppingCart]:
    """
    Returns all shopping carts.
    """
    return ShoppingCart.objects.all()
