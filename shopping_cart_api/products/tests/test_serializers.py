import pytest

from products.serializers import CategorySerializer


@pytest.mark.django_db
class TestCategorySerializer:

    def test_category_can_be_serialized(self, create_category):
        root_category = create_category()
        serialized_category = CategorySerializer(root_category).data
        assert serialized_category['name'] == root_category.name
        assert serialized_category['subcategories'] == []

    def test_category_with_subcategories_can_be_serialized(self, create_category):
        root_category = create_category()
        subcategory = create_category(root_category)
        serialized_category = CategorySerializer(root_category).data
        assert serialized_category['name'] == root_category.name
        assert len(serialized_category['subcategories']) == 1
        assert serialized_category['subcategories'][0]['name'] == subcategory.name
        assert serialized_category['subcategories'][0]['subcategories'] == []
