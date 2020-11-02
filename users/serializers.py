from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from users.models import Address, Phone


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate user with provided email and password')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class AddressEditSerializer(serializers.ModelSerializer):
    city = serializers.CharField(required=False)
    street = serializers.CharField(required=False)

    class Meta:
        model = Address
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user',)
        read_only_fields = ('id',)


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'user', 'number',)
        read_only_fields = ('id',)
