from rest_framework import serializers
from .models import Customer_Accounts,ServiceRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print(email,password,111111111111111111111111111)
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
class CustomerAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_Accounts
        fields = ['full_name','email', 'mobile_no', 'password','address','city','pincode','state','district']
        extra_kwargs = {'password': {'write_only': True}}


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'