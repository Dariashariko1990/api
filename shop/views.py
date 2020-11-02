from django.db import IntegrityError
from django.db.models import Q, ProtectedError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemCreateSerializer, \
    OrderItemEditSerializer
from shop.models import Shop, Category, Product
from shop.serializers import ShopSerializer, CategorySerializer, ProductSerializer


class ShopView(ListAPIView):
    """ Класс для просмотра списка магазинов, принимающих заказы """
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


class CategoryView(ListAPIView):
    """ Класс для просмотра списка всех категорий """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(APIView):
    """ Класс для просмотра товаров (всех, по категории, по магазину или одного по id товара) """

    def get(self, request, *args, **kwargs):

        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')
        product_id = request.query_params.get('product_id')

        if product_id:
            queryset = Product.objects.get(pk=product_id)
            serializer = ProductSerializer(queryset)

        else:
            if shop_id:
                query = query & Q(shop_id=shop_id)

            if category_id:
                query = query & Q(category_id=category_id)

            queryset = Product.objects.filter(
              query).prefetch_related('product_parameters__parameter')

            serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)


class CartView(APIView):
    """ Класс для работы с корзиной пользователя """

    # получить корзину залогиненного пользователя
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)
        basket = Order.objects.filter(
            user_id=request.user.id, state='basket').prefetch_related(
            'items__product__product_parameters__parameter')
        serializer = OrderSerializer(basket, many=True)

        return Response(serializer.data)

    # добавить товар в корзину
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        item = request.data

        basket = Order.objects.get_or_create(user_id=request.user.id, state='basket')[0]
        item.update({'order': basket.id})

        serializer = OrderItemCreateSerializer(data=item)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError as error:
                return Response({'Status': False, 'Errors': str(error)})

            return Response({'Status': True})
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удалить товар из корзины
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        id = request.data['id']
        item = get_object_or_404(OrderItem, pk=id)

        try:
            item.delete()
        except ProtectedError as error:
            return Response({'Status': False, 'Errors': str(error)})

        return Response({'Status': True})

    # изменить кол-во товара в корзине
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        id = request.data['id']
        item = get_object_or_404(OrderItem, pk=id)

        serializer = OrderItemEditSerializer(item, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError as error:
                return Response({'Status': False, 'Errors': str(error)})

            return Response({'Status': True})
        return Response(serializer.errors)










