from rest_framework import serializers

from orders.models import Order, OrderItem
from shop.serializers import ProductSerializer


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'price', 'quantity')
        read_only_fields = ('id',)


class OrderItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'price', 'quantity')
        read_only_fields = ('id',)


class OrderItemEditSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    product = serializers.IntegerField(required=False, max_value=None, min_value=None)
    order = serializers.IntegerField(required=False, max_value=None, min_value=None)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'price', 'quantity')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(read_only=True, many=True)
    total_cost = serializers.IntegerField(
        read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'created', 'state', 'items', 'total_cost')
        read_only_fields = ('id',)