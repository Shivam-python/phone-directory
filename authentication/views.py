from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


# Create your views here.

class Register(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data=request.data

        user_serialized=UserSerializer(data=data)
        if user_serialized.is_valid():
            user_serialized.save()
            return Response(user_serialized.data)
        else:
            return Response(user_serialized.errors,status=400)
        

class Login(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer