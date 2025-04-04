from django.contrib import admin

from products.models import Basket, Product, ProductCategory

# Register your models here.


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'category')
    fields = ('image', 'title', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category')
    search_fields = ('title', 'description')
    ordering = ('-title',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    readonly_fields = ('product', 'quantity',)
    extra = 0
