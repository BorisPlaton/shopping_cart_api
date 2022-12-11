from django.db.models import prefetch_related_objects
from rest_framework import serializers

from eager_loaded_serializer.base import EagerLoadedSerializer
from products.serializers import ProductSerializer
from shopping_cart.models import OrderedProduct, ShoppingCart


class OrderedProductSerializer(serializers.ModelSerializer):
    """
    The serializer for an ordered product.
    """

    slug = serializers.SlugField(source='product.slug')

    class Meta:
        model = OrderedProduct
        fields = ['slug', 'quantity']

    def to_internal_value(self, data):
        """
        Set a `slug` field when data is deserialized.
        """
        deserialized_data = super(OrderedProductSerializer, self).to_internal_value(data)
        deserialized_data['slug'] = deserialized_data.pop('product')['slug']
        return deserialized_data


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    """
    The serializer for the ordered product in the shopping cart.
    """

    product = ProductSerializer()

    class Meta:
        model = OrderedProduct
        fields = ['quantity', 'product']


class ShoppingCartSerializer(EagerLoadedSerializer, serializers.ModelSerializer):
    """
    The serializer for shopping cart with list of ordered products.
    """

    orders = ShoppingCartProductSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['pk', 'orders']

    def setup_eager_loading(self, model: ShoppingCart):
        """
        Prefetches db model data to reduce the number of queries when
        a user has many ordered products.
        """
        prefetch_related_objects([model], 'orders__product')
        # ProductSerializer.setup_eager_loading(model.products)
        return model
