from django.db.models import QuerySet
from django.http import Http404

from products.models import Category, Product


def get_all_root_categories() -> QuerySet[Category]:
    """
    Returns all root categories (Categories which don't
    have parents).
    """
    return Category.objects.filter(level=0).all()


def get_product_by_slug(slug: str) -> Product:
    """
    Returns product or raise an 404 exception if it
    doesn't exist.
    """
    try:
        return Product.objects.get(slug=slug)
    except Product.DoesNotExist as e:
        raise Http404(str(e))
