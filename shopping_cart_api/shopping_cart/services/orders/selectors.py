from authentication.models import CustomUser
from shopping_cart.models import Order


def get_user_orders(user: CustomUser) -> list[Order]:
    """
    Returns all orders that user has performed.
    """
    return user.orders.all()
