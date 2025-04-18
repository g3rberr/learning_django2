import stripe

from django.db import models
from django.urls import reverse
from django.conf import settings

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    stripe_product_price_id = models.CharField(max_length=128, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Продукт: {self.title} | Категория: {self.category.title}'

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)


    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.title)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub')
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return round(sum(basket.sum() for basket in self))

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
               'price': basket.product.stripe_product_price_id,
               'quantity': basket.quantity
            }
            line_items.append(item)
        return line_items
    
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
        return round(self.product.price * self.quantity)

    def de_json(self):
        basket_item = {
            'product_name': self.product.title,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item