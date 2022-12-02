from django.urls import path

from products import views


app_name = 'products'

urlpatterns = [
    path('categories/', views.CategoriesTree.as_view(), name='categories'),
    path('list/<slug:slug>/', views.SpecificProduct.as_view(), name='product')
]
