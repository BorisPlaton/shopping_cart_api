import pytest
from django.urls import reverse
from rest_framework.response import Response


@pytest.mark.django_db
class TestCategoriesTreeView:

    def test_view_returns_empty_list_if_categories_dont_exist(self, api_client):
        response: Response = api_client.get(reverse('products:categories-list'))
        assert not response.data
        assert isinstance(response.data, list)

    def test_if_category_exists_it_will_be_in_response(self, api_client, create_category):
        category = create_category()
        response: Response = api_client.get(reverse('products:categories-list'))
        assert len(response.data) == 1
        assert response.data[0]['name'] == category.name
        assert response.data[0]['subcategories'] == []

    def test_if_category_exists_and_has_subcategories_they_will_be_in_response(self, api_client, create_category):
        root_category = create_category()
        subcategory = create_category(root_category)
        response: Response = api_client.get(reverse('products:categories-list'))
        assert response.status_code == 200
        assert response.data == [{
            "id": root_category.pk,
            "name": root_category.name,
            "subcategories": [
                {
                    "id": subcategory.pk,
                    "name": subcategory.name,
                    "subcategories": []
                }
            ]
        }]

    @pytest.mark.parametrize(
        'http_method',
        ['post', 'put', 'patch', 'delete']
    )
    def test_only_get_method_for_categories_is_available(self, api_client, http_method):
        response = getattr(api_client, http_method)(reverse('products:categories-list'))
        assert response.status_code == 405


@pytest.mark.django_db
class TestSpecificProductView:

    def test_view_returns_404_status_code_if_product_doesnt_exist(self, api_client):
        response: Response = api_client.get(reverse('products:product-detail', args=['wrong-slug']))
        assert response.status_code == 404
        assert response.data.keys() == {'detail'}

    def test_view_returns_specific_product_by_slug_and_200_status_code(self, api_client, create_product):
        product = create_product()
        response: Response = api_client.get(reverse('products:product-detail', args=[product.slug]))
        assert response.status_code == 200
        assert response.data == {
            "id": product.pk,
            "slug": product.slug,
            "name": product.name,
            "categories": [
                {"id": category.pk, "name": category.name} for category in
                product.category.get_ancestors(include_self=True)
            ],
            "description": product.description,
            "price": product.price,
            "rating": product.rating,
        }

    @pytest.mark.parametrize(
        'http_method',
        ['post', 'put', 'patch', 'delete']
    )
    def test_only_get_method_for_product_detail_is_available(self, api_client, http_method, create_product):
        product = create_product()
        response = getattr(api_client, http_method)(reverse('products:product-detail', args=[product.slug]))
        assert response.status_code == 405
