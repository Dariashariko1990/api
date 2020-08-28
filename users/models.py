from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='address', blank=True,
                             on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)

    class Meta:
        verbose_name = 'Адресс пользователя'
        verbose_name_plural = 'Адресса пользователя'

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'


class Phone(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='phone_number', blank=True,
                             on_delete=models.CASCADE)
    number = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Телефон пользователя'
        verbose_name_plural = 'Список телефонов пользователей'

    def __str__(self):
        return self.number
