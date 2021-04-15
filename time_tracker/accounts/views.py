# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import UserLoginRequestSerializer, UserGetallSerializer, UserRegSerializer, \
    UserListSerializer

from .services import UserServices
from .models import User
from libs.constants import BAD_REQUEST, BAD_ACTION, ALREADY_EXIST
from libs.error_messages import ERROR_MESSAGE
from libs.exceptions import ParseException

# Create your views here.
class UserViewSet(GenericViewSet):
    """
    user class
    """
    queryset = User.objects.all().order_by('-created_at')

    services = UserServices()
    filter_backends = (filters.OrderingFilter,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    ordering_fields = ('id',)
    ordering = ('id',)
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put']

    serializers_dict = {
        'login': UserLoginRequestSerializer,
        'register': UserRegSerializer,
        'user_add':UserRegSerializer,
        'user_list': UserListSerializer,
        'user_get': UserListSerializer,
        }


    def get_queryset(self, filterdata=None):
        if filterdata:
            self.queryset = User.objects.filter(**filterdata)
        return self.queryset

    def get_serializer_class(self):
        """
        Returns serializer class
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)


    @action(methods=['post'], detail=False, permission_classes=[])
    def register(self, request):
        """
        Returns user Registration
        """
        # password = self.services.random_password_generation()
        
        serializer = self.get_serializer(data=user)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        if user:
            return Response({"status": "Successfully Registered"}, status=status.HTTP_201_CREATED)
        return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
    

    @action(methods=['post'], detail=False, permission_classes=[])
    def login(self, request):
        """
        Return user login
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            raise ParseException(BAD_REQUEST, serializer.errors)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"])

        if not user:
            return Response({'status': 'Invalid Credentials'},status=status.HTTP_404_NOT_FOUND)


        token = user.access_token
        return Response({'token': token},
                        status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def logout(self, request):
        """
        Return user logout
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

