from shopping_cart.models import ShoppingCart


def get_shopping_cart_by_id(shopping_cart_id: str):
    """
    Returns the shopping cart by its id.
    """
    return ShoppingCart.objects.get(pk=shopping_cart_id)
