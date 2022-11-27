import pytest

from products.services.selectors import get_all_root_categories


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
