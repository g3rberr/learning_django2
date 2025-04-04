from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache


from common.views import TitleMixin

from .models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'
    


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()

        if category_slug := self.request.GET.get('category'):  # ?category=
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(object_list=object_list, **kwargs)
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# def index(request):
#     return render(request, 'products/index.html')


# def products(request, category_slug=None, page_number=1):
#     categories = ProductCategory.objects.all()
#     products = Product.objects.all().select_related('category') # для избежания ненужных запросов в базу данных

#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
#     print(products_paginator, 'aaaaaaaaaaa')
#     if slug:=request.GET.get('category'):
#         products = products.filter(category__slug=slug)

#     return render(request, 'products/products.html', context={'categories': categories,
#                                                             'products': products_paginator
#                                                             })


# def filter_category(request, category_slug):
#     '''Фильтрация по категориям второй метод'''
#     categories = ProductCategory.objects.all()
#     products = Product.objects.filter(category__slug=category_slug)
#     context = {'categories': categories, 'products': products}
#     return render(request, 'products/products.html', context) #много кода но разделение логики является нормой(?) -
#        - в любом случае первый вариант мне больше нравится, тк можно в будущем делать фильтрацию по многим параметрам
