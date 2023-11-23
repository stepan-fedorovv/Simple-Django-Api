from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import CustomUser

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=256, read_only=True, required=False)

    def validate(self, attrs):
        user = CustomUser(**attrs)
        if not attrs.get('username'):
            raise serializers.ValidationError("Username is require")
        if not attrs.get('email'):
            raise serializers.ValidationError("Email is require")

        if not attrs.get('password') or not self.context['request'].data.get('confirm_password'):
            raise serializers.ValidationError("Password and confirm password is requires fields")
        if self.context['request'].data.get('confirm_password') != attrs.get('password'):
            raise serializers.ValidationError("Password missmatch")
        try:
            validate_password(password=attrs.get('password'), user=user)
        except serializers.ValidationError as e:
            raise e
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return CustomUser.objects.create(**validated_data)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'confirm_password', 'password', 'username']


class LoginUserSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class SendRestoreLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=256)

    class Meta:
        model = CustomUser
        fields = ['email']


class RestorePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=256, read_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        user = User(**attrs)
        if not attrs.get('password') or not self.context['request'].data.get('confirm_password'):
            raise serializers.ValidationError("Password and confirm password is requires fields")
        if self.context['request'].data.get('confirm_password') != attrs.get('password'):
            raise serializers.ValidationError("Password missmatch")
        try:
            validate_password(password=attrs.get('password'), user=user)
        except serializers.ValidationError as e:
            raise e
        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data.get('password'))
        instance.save()
        return instance


class UserInformationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256, required=False)
    first_name = serializers.CharField(max_length=256, required=False)
    last_name = serializers.CharField(max_length=256, required=False)
    phone_number = serializers.IntegerField(required=False)
    bio = serializers.CharField(max_length=500, required=False)
    email = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'phone_number', 'bio', 'email']


class UserImageSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ['profile_picture', ]
