# Generated by Django 4.1.3 on 2022-12-11 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('shopping_cart', '0003_alter_orderedproduct_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='products',
            field=models.ManyToManyField(related_name='carts', through='shopping_cart.OrderedProduct', to='products.product'),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='shopping_cart.shoppingcart', verbose_name='Shopping cart'),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='products.product', verbose_name='Product in order'),
        ),
    ]
