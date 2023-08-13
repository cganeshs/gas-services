from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from django.contrib.auth.models import update_last_login
from .loginview import CustomObtainAuthToken
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import ServiceRequest

@api_view(['POST'])
@permission_classes([AllowAny])
def CustomerRegistrationView(request):
    if request.method == 'POST':
        serializer = CustomerAccountsSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Your account has been successfully created on Bynry Gas Services'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(CustomObtainAuthToken):
        def post(self, request, *args, **kwargs):
                try:
                    serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
                    serializer.is_valid(raise_exception=True)
                    user = serializer.validated_data['user']
                    token, created = Token.objects.get_or_create(user=user)
                    update_last_login(None, user)
                    return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                    })

                except Exception as e:
                        print(e)
                        return Response({"message": "Unable to log in with the provided credentials"},status = status.HTTP_400_BAD_REQUEST)

class Logout(generics.ListAPIView):     
    def list(self,request):
            if request.method == 'GET':
                    request.user.auth_token.delete()
                    return Response({'message':'Successfully logout'})
                
class ServiceRequestView(ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(customer=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
