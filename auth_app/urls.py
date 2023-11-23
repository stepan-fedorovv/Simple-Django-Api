from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from .views import UserCredentials, GetCSRFToken, UserInformation, UserImage

urlpatterns = [
    path('register/', UserCredentials.as_view({"post": "register"})),
    path('login/', UserCredentials.as_view({"post": "user_login"})),
    path('reset/link/', UserCredentials.as_view({"post": "create_reset_token"})),
    path('reset/', UserCredentials.as_view({"patch": "restore_user_password"})),
    path('csrf/', GetCSRFToken.as_view({"get": "get_cookie"})),
    path('logout/', UserCredentials.as_view({"post": "user_logout"})),
    path('user/', UserInformation.as_view({"get": "get_current_user"})),
    path('user/change/info/', UserInformation.as_view({"patch": "change_user_base_info"})),
    path('user/change/picture/<str:filename>', UserImage.as_view({"post": "update_user_picture"}))

]
