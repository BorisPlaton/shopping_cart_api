from rest_framework import serializers

from shopping_cart.models import OrderedProduct


class OrderedProductSerializer(serializers.ModelSerializer):
    """
    The serializer for an ordered product.
    """

    product_id = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderedProduct
        fields = ['product_id', 'quantity']
