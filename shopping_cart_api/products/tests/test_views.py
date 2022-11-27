import pytest
from django.urls import reverse
from rest_framework.response import Response


@pytest.mark.django_db
class TestCategoriesTreeView:

    def test_view_returns_empty_list_if_categories_dont_exist(self, api_client):
        response: Response = api_client.get(reverse('products:categories'))
        assert not response.data
        assert isinstance(response.data, list)

    def test_if_category_exists_it_will_be_in_response(self, api_client, create_category):
        category = create_category()
        response: Response = api_client.get(reverse('products:categories'))
        assert len(response.data) == 1
        assert response.data[0]['name'] == category.name
        assert response.data[0]['subcategories'] == []

    def test_if_category_exists_and_has_subcategories_they_will_be_in_response(self, api_client, create_category):
        root_category = create_category()
        subcategory = create_category(root_category)
        response: Response = api_client.get(reverse('products:categories'))
        assert len(response.data) == 1
        assert response.data[0]['name'] == root_category.name
        assert response.data[0]['subcategories'][0]['name'] == subcategory.name
        assert response.data[0]['subcategories'][0]['subcategories'] == []
