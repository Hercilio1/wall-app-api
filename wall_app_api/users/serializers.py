from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)
        read_only_fields = ('email', )


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, data):
        user = User(**data)

        password = data.get('password')

        errors = dict()
        try:
            password_validation.validate_password(password=password, user=user)

        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(CreateUserSerializer, self).validate(data)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
