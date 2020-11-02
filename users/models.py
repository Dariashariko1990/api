
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Кастомная модель пользователя, заменяющая username на email """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        send_mail(
            'Registration completed',
            'You have been successfully registered at our service.',
            'from@example.com',
            [self.email]
        )


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
