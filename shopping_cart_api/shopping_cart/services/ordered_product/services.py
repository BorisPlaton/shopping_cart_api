from products.services.selectors import get_products_by_ids
from shopping_cart.models import ShoppingCart, OrderedProduct


def create_ordered_products(shopping_cart: ShoppingCart, products_info: list[dict]):
    """
    Creates new ordered products and adds them to already existing shopping cart.
    """
    products_records = get_products_by_ids([product['product_id'] for product in products_info])
    return OrderedProduct.objects.bulk_create([
        OrderedProduct(
            cart=shopping_cart, product=products_records.get(pk=data['product_id']), quantity=data['quantity']
        ) for data in products_info if data['product_id'] in products_records.values_list('pk', flat=True)
    ])
