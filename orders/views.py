from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import ProtectedError, Count, Sum, F, FloatField
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers import OrderSerializer
from users.models import User, Address, Phone
from users.serializers import AddressSerializer, AddressEditSerializer, PhoneSerializer
from rest_framework import viewsets, status


class OrdersView(APIView):
    """ Класс для работы с заказами """

    # Получить все заказы, один по id, по id пользователя или магазина
    def get(self, request, *args, **kwargs):
        order_id = request.query_params.get('order_id')
        user_id = request.query_params.get('user_id')
        shop_id = request.query_params.get('shop_id')

        if order_id:
            queryset = Order.objects.filter(pk=order_id).prefetch_related('items').annotate(
                total_cost=Sum(F('items__price') * F("items__quantity"), output_field=FloatField()))

        elif user_id:
            user = User.objects.get(pk=user_id)
            queryset = Order.objects.filter(user=user).prefetch_related('items').annotate(
                total_cost=Sum(F('items__price') * F("items__quantity"), output_field=FloatField()))

        elif shop_id:
            queryset = Order.objects.filter(items__product__shop=shop_id).prefetch_related('items').annotate(
                total_cost=Sum(F('items__price') * F("items__quantity"), output_field=FloatField()))

        else:
            queryset = Order.objects.all().prefetch_related('items').annotate(
                total_cost=Sum(F('items__price') * F("items__quantity"), output_field=FloatField()))

        serializer = OrderSerializer(queryset, many=True)

        return Response(serializer.data)

    # Изменить статус заказа, разместить заказ из корзины.
    # При изменении статуса на confirmed отправляет email с подтверждением заказа на почту покупателя.
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        order_id = request.data['id']

        order = get_object_or_404(Order, pk=order_id)
        update_order = request.data
        update_order.update({'user': request.user.id})

        serializer = OrderSerializer(order, data=update_order)
        if serializer.is_valid():
            try:
                serializer.save()
                if request.data['state'] == 'confirmed':
                    send_mail(
                        'Order confirmed',
                        'Thank you for your order!',
                        'from@example.com',
                        [request.user.email]
                    )
            except IntegrityError as error:
                return Response({'Status': False, 'Errors': str(error)})

            return Response({'Status': True})
        return Response(serializer.errors)


class ContactView(APIView):
    """ Класс для работы с адрессами покупателей """

    # получить контакты залогиненного пользователя
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=401)

        contact = Address.objects.filter(
            user_id=request.user.id)
        serializer = AddressSerializer(contact, many=True)
        return Response(serializer.data)

    # добавить новый адрес
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        address = request.data
        user_id = request.user.id
        address.update({'user': user_id})

        serializer = AddressSerializer(data=address)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError as error:
                return Response({'Status': False, 'Errors': str(error)})

            return Response({'Status': True})
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # редактировать адресс
    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        id = request.data['id']
        address = get_object_or_404(Address, pk=id)

        serializer = AddressEditSerializer(address, data=request.data, )

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError as error:
                return Response({'Status': False, 'Errors': str(error)})

            return Response({'Status': True})
        return Response(serializer.errors)

    # удалить адресс
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        id = request.data['id']
        address = get_object_or_404(Address, pk=id)

        try:
            address.delete()
        except ProtectedError as error:
            return Response({'Status': False, 'Errors': str(error)})

        return Response({'Status': True})


class PhoneView(APIView):
    """ Класс для работы с телефоном покупателей """

    # получить записи телефонов пользователя
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        phone = Phone.objects.filter(
            user_id=request.user.id)
        serializer = PhoneSerializer(phone, many=True)
        return Response(serializer.data)

    # добавить новый телефон
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        phone = request.data
        user_id = request.user.id
        phone.update({'user': user_id})

        serializer = PhoneSerializer(data=phone)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError as error:
                return Response({'Status': False, 'Errors': str(error)})

            return Response({'Status': True})
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # редактировать телефон
    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        id = request.data['id']
        phone = get_object_or_404(Phone, pk=id)

        serializer = PhoneSerializer(phone, data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError as error:
                return Response({'Status': False, 'Errors': str(error)})

            return Response({'Status': True})
        return Response(serializer.errors)

    # удалить телефон
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        id = request.data['id']
        phone = get_object_or_404(Phone, pk=id)

        try:
            phone.delete()
        except ProtectedError as error:
            return Response({'Status': False, 'Errors': str(error)})

        return Response({'Status': True})


# Использование viewsets вместо views
class PhoneViewSet(viewsets.ModelViewSet):
    """ Класс для работы с телефоном покупателей """
    serializer_class = PhoneSerializer

    # Переопределяем для работы с телефонами только залогиненного пользователя
    def get_queryset(self):
        return self.request.user.phone_number.all()