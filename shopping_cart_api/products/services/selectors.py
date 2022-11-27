from django.db.models import QuerySet

from products.models import Category


def get_all_root_categories() -> QuerySet[Category]:
    """
    Returns all root categories (Categories which don't
    have parents).
    """
    return Category.objects.filter(level=0).all()
