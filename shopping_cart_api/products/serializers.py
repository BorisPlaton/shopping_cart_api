from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
