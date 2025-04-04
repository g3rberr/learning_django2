from http import HTTPStatus

from django.test import TestCase, RequestFactory
from django.urls import reverse

from users.models import User
from products.models import Product, ProductCategory
from products.views import ProductListView

# Впервые пишу тесты лл, выглядит интересно

class IndexListViewTestCase(TestCase):
    
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')



class ProductsListViewTestCase(TestCase):
    fixtures = ['/home/miserable/backend-learning/myprojects/learning-django/store1/store-project/store/products/fixtures/categories.json',
            '/home/miserable/backend-learning/myprojects/learning-django/store1/store-project/store/products/fixtures/goods.json']

    def setUp(self):
        self.factory = RequestFactory()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        products = Product.objects.all()
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data['object_list']), list(products[:3]))
        
    def test_list_with_category(self):
        test_category = ProductCategory.objects.last()
        request = self.factory.get('/products/', {'category': test_category.slug}) # ?category={slug}
        
        view = ProductListView()
        view.request = request
        queryset = view.get_queryset()
        expected_products = Product.objects.filter(category=test_category)
        self.assertEqual(list(queryset), list(expected_products))


# class ProductListViewTestCase(TestCase):
#     fixtures = ['products/fixtures/categories.json', 'products/fixtures/goods.json']

#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_list(self):
#         path = reverse('products:index')
#         response = self.client.get(path)
#         products = Product.objects.all()

#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(response.context_data['title'], 'Store - Каталог')
#         self.assertTemplateUsed(response, 'products/products.html')
#         self.assertEqual(list(products[:3]), response.)