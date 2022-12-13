from rest_framework.exceptions import NotFound, ValidationError

from shopping_cart.models import ShoppingCart, OrderedProduct
from shopping_cart.services.shopping_cart.cart_cookie_manager import CartCookieManager
from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_by_id, get_shopping_cart_id_from_cookies


def get_or_create_shopping_cart_from_cookies(request_cookies: dict) -> ShoppingCart:
    """
    Returns a shopping cart from the cookies. If the cookie or the
    shopping cart doesn't exist, it will create a new one.
    """
    shopping_cart_id = get_shopping_cart_id_from_cookies(request_cookies)
    if not shopping_cart_id:
        return create_shopping_cart()
    try:
        return get_shopping_cart_by_id(shopping_cart_id)
    except (NotFound, ValidationError):
        return create_shopping_cart()


def update_products_quantity_in_cart(cart: ShoppingCart, update_products_info: list[dict]):
    """
    Updates product quantity in the shopping cart.
    """
    product_slug_with_updated_quantity = {
        product['slug']: product['quantity'] for product in update_products_info
    }
    altered_products = []
    for ordered_product in cart.ordered_products.filter(product__slug__in=product_slug_with_updated_quantity):
        ordered_product.quantity = product_slug_with_updated_quantity[ordered_product.product.slug]
        altered_products.append(ordered_product)
    OrderedProduct.objects.bulk_update(altered_products, ['quantity'])
    return altered_products


def delete_products_from_shopping_cart(cart: ShoppingCart, products_to_delete: list[dict]):
    """
    Deletes products from shopping cart. Affects only those records, which
    are in the `products_to_delete` argument.
    """
    deleted_products = cart.ordered_products.filter(
        product__slug__in=[product['slug'] for product in products_to_delete]
    )
    return deleted_products.delete()[0]


def create_shopping_cart() -> ShoppingCart:
    """
    Creates and returns new shopping cart instance.
    """
    return ShoppingCart.objects.create()


def set_shopping_cart_id_cookie(response_cookies: dict, shopping_cart: ShoppingCart):
    """
    Sets a cookie with the cart id.
    """
    return CartCookieManager(response_cookies).set_shopping_cart_id(str(shopping_cart.pk))
