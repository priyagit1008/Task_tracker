from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from django.core.validators import validate_email

from django.contrib.postgres.fields import ArrayField

# from libs.helpers import time_it

from .models import User

class UserLoginRequestSerializer(serializers.ModelSerializer):
    """
    UserLoginSerializer
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'access_token')


class UserVerifyRequestSerializer(serializers.Serializer):
    """
    UserLoginSerializer
    """
    email = serializers.SerializerMethodField()
    otp = serializers.CharField()


class UserRegSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=False, min_length=5)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    mobile = serializers.IntegerField(required=True)
    dob = serializers.DateField(input_formats=['%d-%m-%Y', ], required=False)
    gender = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    pincode = serializers.CharField(required=False)
    qualification = serializers.CharField(required=False)
    status = serializers.CharField(required=False)



    def validate(self, data):
        user_obj = self.Meta.model(**data)
        user_obj.full_clean()
        return data
    
   
    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)
        # read_only_fields = ('id',)
    


    # @time_it
    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user





class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserGetallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


