from django.urls import path
from rest_framework.routers import DefaultRouter

from shopping_cart import views


app_name = 'shopping_cart'
router = DefaultRouter()
router.include_root_view = False
router.register('', views.ShoppingCartView, basename='cart')

urlpatterns = [
    path('orders/', views.UserOrdersView.as_view(), name='order-create'),
    *router.urls,
]
