from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer

from backend.external_requests import verify_email, auto_user_info
from backend.models import User, Post
from django.core.exceptions import ValidationError
from rest_framework import serializers


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        auto_name = None
        try:
            validate_password(validated_data['password'])
        except ValidationError as error:
            raise serializers.ValidationError({'Status': False, 'Errors': f'{error}'})
        verify_email_status = verify_email(validated_data["email"])
        if verify_email_status != 'valid':
            raise serializers.ValidationError({'Status': False, 'Error': f'Enter your active corporate email'})
        auto_name_info = auto_user_info(validated_data["email"]).get('person')
        if auto_name_info:
            auto_name = auto_name_info['name']['fullName']
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            name=auto_name
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text', 'user']
