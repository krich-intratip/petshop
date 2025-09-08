from django.urls import path
from .views import (
    product_detail, 
    category
)


urlpatterns = [
    path('<slug:slug>/', category, name='category'),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
]