from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.serializers import CategorySerializer
from products.services.selectors import get_all_root_categories


class CategoriesTree(APIView):
    """Views all products categories."""

    def get(self, request: Request):
        """
        Returns all categories and their siblings as
        list of objects.
        """
        return Response(
            CategorySerializer(get_all_root_categories(), many=True).data
        )
