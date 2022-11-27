import uuid

import pytest

from products.models import Category


@pytest.fixture
def create_category():
    def inner(parent_category: Category = None) -> Category:
        return Category.objects.create(name=uuid.uuid4().hex, parent_category=parent_category)

    return inner
