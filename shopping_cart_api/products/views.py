from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.serializers import CategorySerializer
from products.services.selectors import get_all_root_categories


class CategoriesTree(APIView):
    """
    Returns a list of all product categories in hierarchical
    order.
    """

    def get(self, request: Request):
        """
        Returns all categories and their siblings as
        list of objects.
        """
        return Response(
            CategorySerializer(get_all_root_categories(), many=True).data
        )


class SpecificProduct(APIView):
    """Returns a specific product by its slug."""

    def get(self, request: Request, slug: str):
        """Returns product data if it exists."""
        pass
