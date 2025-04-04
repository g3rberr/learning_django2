from django.urls import path
# from django.views.decorators.cache import cache_page

from products.views import ProductListView, basket_add, basket_remove



app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    # path('paginator/<int:page_number>/', products, name='paginator'),
    # path('category/<slug:category_slug>/', filter_category, name='filter_category'),
    path('basket/add/<int:product_id>', basket_add, name='basket_add'),
    path('backets/remove/<int:basket_id>', basket_remove, name='basket_remove'),
]
