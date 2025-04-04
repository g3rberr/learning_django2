from django.db import models
from django.urls import reverse

from users.models import User


# Модель категорий
class ProductCategory(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'


# Модель продуктов
class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='products')

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Продукт: {self.title} | Категория: {self.category.title}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    '''Модель для корзины'''
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.email} | Продукт: {self.product.title}'

    def sum(self):
        return self.product.price * self.quantity

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum([basket.sum() for basket in baskets])

    # def total_quantity(self):
    #     baskets = Basket.objects.filter(user=self.user)
    #     return sum([basket.quantity for basket in baskets])
