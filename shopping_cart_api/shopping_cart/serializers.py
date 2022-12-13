from django.db.models import prefetch_related_objects
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

from eager_loaded_serializer.mixin import EagerLoadedSerializerMixin
from products.serializers import ProductSerializer
from shopping_cart.models import OrderedProduct, ShoppingCart


class MultipleOrderedProductSerializer(ListSerializer):
    """
    The list serializer validates that slug fields are unique
    in the list of data.
    """

    def validate(self, data):
        """
        Validates that slug field is unique among list of
        data.
        """
        product_slugs = [product['slug'] for product in data]
        if len(product_slugs) != len(set(product_slugs)):
            raise ValidationError("You have duplicated product slugs.")
        return data


class SpecificOrderedProductSerializer(serializers.ModelSerializer):
    """
    Serializes specific ordered product from the shopping cart.
    """

    slug = serializers.SlugField(source='product.slug')

    class Meta:
        model = OrderedProduct
        fields = ['slug']
        list_serializer_class = MultipleOrderedProductSerializer

    def to_internal_value(self, data):
        """
        Set a `slug` field when data is deserialized.
        """
        deserialized_data = super().to_internal_value(data)
        deserialized_data['slug'] = deserialized_data.pop('product')['slug']
        return deserialized_data


class OrderedProductSerializer(SpecificOrderedProductSerializer):
    """
    The serializer for the orders with additional `quantity` field.
    """

    class Meta(SpecificOrderedProductSerializer.Meta):
        fields = SpecificOrderedProductSerializer.Meta.fields + ['quantity']


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    """
    The serializer for the ordered product in the shopping cart.
    """

    product = ProductSerializer()

    class Meta:
        model = OrderedProduct
        fields = ['quantity', 'product']


class ShoppingCartSerializer(EagerLoadedSerializerMixin, serializers.ModelSerializer):
    """
    The serializer for shopping cart with list of ordered products.
    """

    orders = ShoppingCartProductSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['pk', 'orders']

    @staticmethod
    def setup_eager_loading(value: ShoppingCart, many):
        """
        Prefetches db model data to reduce the number of queries when
        a user has many ordered products.
        """
        prefetch_related_objects(
            [value], 'orders__product__category__parent_category__parent_category__parent_category'
        )
        return value
