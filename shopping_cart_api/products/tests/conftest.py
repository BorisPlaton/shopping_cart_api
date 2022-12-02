import uuid

import pytest
from model_bakery import baker

from products.models import Category, Product


@pytest.fixture
def create_category():
    def inner(parent_category: Category = None) -> Category:
        return Category.objects.create(name=uuid.uuid4().hex, parent_category=parent_category)

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
