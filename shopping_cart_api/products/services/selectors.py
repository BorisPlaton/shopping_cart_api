from django.db.models import QuerySet
from rest_framework.exceptions import NotFound

from products.models import Category, Product


def get_all_root_categories() -> QuerySet[Category]:
    """
    Returns all root categories (Categories which don't
    have parents).
    """
    return Category.objects.filter(level=0).all()


def get_product_by_slug(slug: str) -> QuerySet[Product]:
    """
    Returns product or raise an 404 exception if it
    doesn't exist.
    """
    try:
        return Product.objects.select_related('category').get(slug=slug)
    except Product.DoesNotExist:
        raise NotFound("Product with slug '%s' doesn't exist." % slug)
