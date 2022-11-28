import pytest
from django.http import Http404
from model_bakery import baker

from products.models import Product
from products.services.selectors import get_all_root_categories, get_product_by_slug


@pytest.mark.django_db
class TestCategorySelectors:

    def test_get_all_root_categories_returns_empty_queryset_if_none_exists(self):
        categories = get_all_root_categories()
        assert not categories.exists()

    def test_get_all_root_categories_returns_only_top_level_categories(self, create_category):
        top_level_category = create_category()
        subcategory = create_category(top_level_category)
        root_categories = get_all_root_categories()
        assert root_categories.exists()
        assert len(root_categories) == 1
        assert top_level_category in root_categories
        assert subcategory not in root_categories


@pytest.mark.django_db
class TestProductSelectors:

    def test_get_product_by_slug_raise_404_exception_if_none_exists(self):
        with pytest.raises(Http404) as e:
            get_product_by_slug("not-existed-slug")
        assert str(e.value) == "Product matching query does not exist."

    def test_specific_product_is_returned_by_its_slug(self, create_category):
        product = baker.make(Product, slug=None, category=create_category(create_category()))
        assert product == get_product_by_slug(product.slug)
