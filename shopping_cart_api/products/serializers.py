from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TreeCategorySerializer(CategorySerializer):
    subcategories = RecursiveField(many=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['subcategories']


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'slug', 'name', 'categories', 'description', 'price', 'rating'
        ]

    def get_categories(self, obj: Product):
        return [
            CategorySerializer(category).data for category
            in obj.category.get_ancestors(include_self=True)
        ]
