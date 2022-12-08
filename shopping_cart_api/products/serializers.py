from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes the Category model.
    """

    class Meta:
        model = Category
        fields = ['id', 'name']


class TreeCategorySerializer(CategorySerializer):
    """
    Serializes categories as a tree structure. Starts from root to the leafs.
    """

    subcategories = RecursiveField(many=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['subcategories']

    @staticmethod
    def setup_eager_loading(queryset: QuerySet[Category]):
        """
        Loads all subcategories to prevent the N+1 problem.
        """
        return queryset.prefetch_related(
            'subcategories__subcategories__subcategories'
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializes the Product model.
    """

    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'slug', 'name', 'categories',
            'description', 'price', 'rating',
        ]

    @staticmethod
    def setup_eager_loading(queryset: QuerySet[Category]):
        """
        Loads all categories and their parent categories to prevent
        the N+1 problem.
        """
        return queryset.prefetch_related(
            'category__parent_category__parent_category'
        )

    def get_categories(self, obj: Product):
        def serialize_category(category: Category) -> list:
            """
            We define an inner function to make a common interface for
            serialization of the Category model.

            The Product model has a `category` field when the Category model
            has a `parent_category`. So, we use it to serialize both of them.
            """
            return [
                CategorySerializer(category).data, *serialize_category(category.parent_category)
            ] if category is not None else []

        return serialize_category(obj.category)[::-1]
