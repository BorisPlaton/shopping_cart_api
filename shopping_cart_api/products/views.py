from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from products.filters import ProductFilter
from products.serializers import TreeCategorySerializer, ProductSerializer
from products.services.selectors import get_all_root_categories, get_product_by_slug, get_all_products


class CategoriesTreeView(APIView):
    """
    Returns a list of all product categories in hierarchical
    order.
    """

    def get(self, request: Request):
        """
        Returns all categories and their descendants as
        list of objects.
        """
        eager_loaded_queryset = TreeCategorySerializer.setup_eager_loading(get_all_root_categories())
        return Response(TreeCategorySerializer(eager_loaded_queryset, many=True).data)


class ProductView(GenericViewSet):
    """
    Handles the Product model.
    """

    queryset = get_all_products()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    lookup_field = 'slug'

    def retrieve(self, request: Request, slug: str):
        """
        Tries to find a specific product by its slug and returns it.
        Otherwise, a response with a 404 status code is returned.
        """
        return Response(ProductSerializer(get_product_by_slug(slug)).data)

    def list(self, request: Request):
        """
        Filters products by given conditions and returns list of them.
        If none was matched, returns an empty list.
        """
        eager_loaded_queryset = ProductSerializer.setup_eager_loading(self.filter_queryset(self.get_queryset()))
        return Response(ProductSerializer(eager_loaded_queryset, many=True).data)
