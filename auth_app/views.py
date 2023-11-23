from django.contrib.auth import login, authenticate, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import RegisterUserSerializer, LoginUserSerializer, RestorePasswordSerializer, \
    SendRestoreLinkSerializer, UserInformationSerializer, UserImageSerializer
from .models import CustomUser, Products


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(GenericViewSet):
    permission_classes = [AllowAny, ]

    def get_cookie(self, request):
        return Response({"success": "CSRF Cookie Set"})


@method_decorator(csrf_protect, name='dispatch')
class UserCredentials(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny, ]
    register_user_serializer = RegisterUserSerializer
    login_serializer = LoginUserSerializer
    email_serializer = SendRestoreLinkSerializer
    restore_password_serializer = RestorePasswordSerializer
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.request.data.get('username'))
        return user

    def get_email_queryset(self):
        user = get_object_or_404(CustomUser, email=self.request.data.get('email'))
        return user

    def register(self, request, *args, **kwargs):
        self.serializer_class = self.register_user_serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
        if user is not None:
            if user.is_active:
                login(request, user)
        return Response({"email": user.email, "username": user.username},
                        status=status.HTTP_201_CREATED)

    def user_login(self, request, *args, **kwargs):
        self.serializer_class = self.login_serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
        if user is not None:
            if user.is_active:
                login(request, user)
        else:
            return Response("Invalid credentials")
        return Response({"email": user.email, "username": user.username}, status=status.HTTP_200_OK)

    def restore_user_password(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        self.serializer_class = self.restore_password_serializer
        instance = request.user
        serializer = self.get_serializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"status": "updated"}, status=status.HTTP_200_OK)

    def user_logout(self, request):
        logout(request)
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class UserInformation(GenericViewSet, UpdateModelMixin, DestroyModelMixin, ListModelMixin):
    serializer_class = UserInformationSerializer
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        user = self.queryset.filter(id=self.request.user.id)
        return user

    def get_current_user(self, request):
        user = self.get_queryset()
        serializer = self.get_serializer(user.values().first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def change_user_base_info(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance=self.request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class UserImage(GenericViewSet, UpdateModelMixin):
    parser_classes = (MultiPartParser,)
    serializer_class = UserImageSerializer
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        user = self.queryset.get(id=self.request.user.id)
        return user

    def update_user_picture(self, request, filename, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_queryset()
        serializer = self.serializer_class(instance=user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
