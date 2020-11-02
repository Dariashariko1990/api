from distutils.util import strtobool

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import get
from yaml import load as load_yaml, Loader

from orders.models import Order
from orders.serializers import OrderSerializer
from shop.models import Shop, Category, Product, Parameter, ProductParameter
from shop.serializers import ShopSerializer


class PartnerUpdate(APIView):
    """ Класс для импорта прайса от поставщика """

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        # if request.user.type != 'shop':
        #    return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                data = load_yaml(stream, Loader=Loader)

                shop = Shop.objects.get_or_create(name=data['shop'])[0]

                for category in data['categories']:
                    category_object = Category.objects.get_or_create(id=category['id'], name=category['name'])[0]
                    category_object.shops.add(shop.id)
                    category_object.save()

                for item in data['goods']:

                    product = Product.objects.create(external_id=item['id'],
                                                     category_id=item['category'],
                                                     model=item['model'],
                                                     name=item['name'],
                                                     price=item['price'],
                                                     price_rrc=item['price_rrc'],
                                                     quantity=item['quantity'],
                                                     shop_id=shop.id)

                    for name, value in item['parameters'].items():
                        parameter_object = Parameter.objects.get_or_create(name=name)[0]
                        ProductParameter.objects.create(product_id=product.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return Response({'Status': True})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class PartnerState(APIView):
    """ Класс для получения статуса партнера """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        try:
           shop = request.user.shop
        except Shop.DoesNotExist as error:
            return Response({'Status': False, 'Errors': str(error)})

        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        state = request.data.get('state')
        if state:
            try:
                Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
            except AttributeError as error:
                return Response({'Status': False, 'Errors': str(error)})
            return Response({'Status': True})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class PartnerOrders(APIView):
    """ Класс для получения заказов поставщиками """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        else:
            queryset = Order.objects.filter(
               items__product__shop__user_id=request.user.id
            )

            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data)