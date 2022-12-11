from django.db import IntegrityError

from exceptions.http_exceptions import StateConflict
from products.services.selectors import get_product_by_slug
from shopping_cart.models import ShoppingCart, OrderedProduct


def create_ordered_product(shopping_cart: ShoppingCart, product_info: dict) -> OrderedProduct:
    """
    Creates new ordered product and adds it to the already
    existing shopping cart. If the product is already in the
    cart, exception is raised.
    """
    product_slug = product_info['slug']
    try:
        return OrderedProduct.objects.create(
            product=get_product_by_slug(product_slug),
            cart=shopping_cart,
            quantity=product_info['quantity'],
        )
    except IntegrityError:
        raise StateConflict(
            "You already have a product with slug %s in your cart. "
            "You may update its quantity or delete it."
            % product_slug
        )
