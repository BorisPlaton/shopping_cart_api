import uuid
from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product


class ShoppingCart(models.Model):
    """
    The shopping cart.
    """

    id = models.UUIDField("Cart id", primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "Shopping cart"
        verbose_name_plural = "Shopping carts"

    @property
    def last_updated_at(self) -> datetime | None:
        """
        Returns the date when the cart was last updated. If the cart doesn't
        have products, returns none.
        """
        try:
            return self.ordered_products.latest('updated_at').updated_at
        except OrderedProduct.DoesNotExist:
            return None

    def __str__(self):
        return str(self.id)


class OrderedProduct(models.Model):
    """
    The ordered product information.
    """

    cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, verbose_name="Shopping cart", related_name='ordered_products'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Product in order", related_name='ordered_products'
    )
    quantity = models.IntegerField("Products amount", validators=[MinValueValidator(1)])
    updated_at = models.DateTimeField("Last updated at", auto_now=True)

    class Meta:
        verbose_name = "Ordered product"
        verbose_name_plural = "Ordered products"
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=1), name='product_quantity_is_natural_int'
            ),
            models.UniqueConstraint(
                fields=['cart', 'product'], name='unique_product_for_cart'
            )
        ]
