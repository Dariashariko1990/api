from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers import OrderSerializer


class OrdersView(APIView):
    def get(self, request, *args, **kwargs):
        order_id = request.query_params.get('order_id')

        if order_id:
            queryset = Order.objects.get(pk=order_id)
            serializer = OrderSerializer(queryset)

        else:
            queryset = Order.objects.all().prefetch_related('items')
            serializer = OrderSerializer(queryset, many=True)

        return Response(serializer.data)



