from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.serializers import TreeCategorySerializer, ProductSerializer
from products.services.selectors import get_all_root_categories, get_product_by_slug


class CategoriesTree(APIView):
    """
    Returns a list of all product categories in hierarchical
    order.
    """

    def get(self, request: Request):
        """
        Returns all categories and their descendants as
        list of objects.
        """
        return Response(
            TreeCategorySerializer(get_all_root_categories(), many=True).data
        )


class SpecificProduct(APIView):
    """Returns data about specific product."""

    def get(self, request: Request, slug: str):
        """Returns specific product data if it exists using slug."""
        return Response(
            ProductSerializer(get_product_by_slug(slug)).data
        )
