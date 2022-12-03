import uuid

import pytest
from model_bakery import baker

from products.models import Category, Product


@pytest.fixture
def create_category():
    def inner(parent_category: Category = None, **kwargs) -> Category:
        kwargs.setdefault('name', uuid.uuid4().hex)
        return Category.objects.create(parent_category=parent_category, **kwargs)

    return inner


@pytest.fixture
def create_product(create_nested_category):
    def inner(**kwargs) -> Product:
        return baker.make(Product, slug=None, category=create_nested_category(2), **kwargs)

    return inner


@pytest.fixture
def create_nested_category(create_category):
    def inner(category_level=1) -> Category:
        category = None
        for _ in range(category_level + 1):
            category = create_category(category)
        return category

    return inner
