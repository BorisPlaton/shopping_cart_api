import pytest
from rest_framework.exceptions import NotFound

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
        with pytest.raises(NotFound) as e:
            get_product_by_slug("not-existed-slug")
        assert e.value.status_code == 404

    def test_specific_product_is_returned_by_its_slug(self, create_product):
        product = create_product()
        assert product == get_product_by_slug(product.slug)
