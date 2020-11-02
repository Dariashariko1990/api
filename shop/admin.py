from django.contrib import admin

from shop.models import Category, Shop, Product


class CategoryShopInline(admin.TabularInline):
    model = Shop.categories.through


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['name', ]
    inlines = [CategoryShopInline]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['name', 'state']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['name']




