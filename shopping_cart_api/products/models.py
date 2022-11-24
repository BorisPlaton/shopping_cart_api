from autoslug import AutoSlugField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class Category(MPTTModel):
    """The product category model."""

    name = models.CharField("Category name", max_length=32, unique=True)
    parent_category = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='subcategories', verbose_name="Parent category"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

        constraints = [
            models.CheckConstraint(
                check=models.Q(level__lte=2), name="depth_level_is_lte_2"
            )
        ]

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'parent_category'


class Product(models.Model):
    """The shop product model."""

    name = models.CharField("Product name", max_length=64)
    slug = AutoSlugField(
        "Product slug", populate_from='name', allow_unicode=True,
        max_length=256, unique=True
    )
    description = models.TextField("Product description")
    categories = TreeManyToManyField(
        Category, related_name='products', verbose_name="Product categories"
    )
    price = models.PositiveIntegerField("Product price")
    rating = models.PositiveIntegerField("Product rating")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
