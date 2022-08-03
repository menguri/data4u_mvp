from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from accounts.forms import UserForm
import os
import requests
import time
from django.conf import settings
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from ..serializers import *
# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)	#사용자 인증
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {'form':form})


# kakao 로그인
KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": '0a32dcc9e9e21081bf2ca1260b837ae8',
    "KAKAO_REDIRECT_URI": "https://practice-poll.run.goorm.io/accounts/login/kakao/callback/",
    "KAKAO_CLIENT_SECRET_KEY": 'eBdC1RIvBxKDb0haUWHQNNRIHmFmjYmr', 
}

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"