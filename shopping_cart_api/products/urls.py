from django.urls import path

from products import views


app_name = 'products'

urlpatterns = [
    path('categories/', views.CategoriesTree.as_view(), name='categories'),
    path('products/<slug:slug>', views.CategoriesTree.as_view(), name='categories')
]
