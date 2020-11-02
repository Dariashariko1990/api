from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemsInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['user', 'created', 'state']
    inlines = [OrderItemsInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['order', 'product']





