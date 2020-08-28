from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Shop, Category, Product
from shop.serializers import ShopSerializer, CategorySerializer, ProductSerializer


class ShopView(ListAPIView):
    """
    Класс для просмотра списка магазинов, принимающих заказы
    """
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


class CategoryView(ListAPIView):
    """
    Класс для просмотра списка всех категорий
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(APIView):
    """
    Класс для просмотра товаров (всех, по категории, по магазину или одного по id товара)
    """

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

            # фильтруем и отбрасываем дуликаты
            queryset = Product.objects.filter(
              query).select_related(
              'shop', 'category').distinct()

            serializer = ProductSerializer(queryset, many=True)

        # .prefetch_related('product_parameters__parameter')

        return Response(serializer.data)
