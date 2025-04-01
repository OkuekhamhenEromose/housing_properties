
# from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from . serializers import UserSerializer,RegistrationSerializer,UpdateProfileSerializer
from . models import Profile
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login,logout

# registration
class RegistrationView(APIView):
    # def get(self,request):
    #     if request.user.is_authenticated:
    #         return redirect('dashboard')
    def post(self,request):
        try:
            if request.user.is_authenticated:
                return Response({"Message":"You are logged in already"})
            
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Login
class LoginView(APIView):
    def post(self,request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return Response({"Message":"User login successfully!"}, status=status.HTTP_200_OK)
            return Response({"Message":"username/password not correct"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
# Logout
class LogoutView(APIView):
    def post(self,request):
        try:
            logout(request)
            return Response({"Message":"Logout Successful!"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# dashboard
@permission_classes([IsAuthenticated])
class DashboardView(APIView):
    def get(self,request):
        try:
            user = request.user.profile
            return Response({"Message": "welcome" +" "+ user.fullname})
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# update
class UpdateProfileView(APIView):
    def get(self,request):
        try:
            profile = request.user.profile
            serializer = UpdateProfileSerializer(profile)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request):
        try:
            profile = request.user.profile
            serializer = UpdateProfileSerializer(profile,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateProfileView(APIView):
    def get(self,request):
        try:
            profile = request.user.profile
            serializer = UpdateProfileSerializer(profile)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request):
        try:
            profile = request.user.profile
            serializer = UpdateProfileSerializer(profile,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)






# from django.shortcuts import redirect

# from rest_framework.views import APIView
# from rest_framework import serializers,status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated#when logged in, user shouldnt see register page. This is used to solve that
# from rest_framework.decorators import permission_classes#decorators must have @

# from .serializers import UserSerializer,RegistrationSerializer#,UpdateProfileSerializer
# from . models import Profile
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# # Create your views here.


# class RegistrationView(APIView):
#     def get(self,request):# to redirect page to dashboard
#         if request.user.is_authenticated:
#             return redirect('dashboard')
#     def post(self,request):
#         try:
#             if request.user.is_authenticated:
#                 return Response({"Message":"You are logged in already"})
#             serializer = RegistrationSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class LoginView(APIView):
#     def post(self,request):

#         try:
#             username = request.data.get('username')
#             password = request.data.get('password')
#             user = authenticate(username=username,password=password)
#             if user is not None:#if user is registered
#                 login(request,user)
#                 return Response({"Message":"User login successfully!"}, status=status.HTTP_200_OK)
#             return Response({"Message":"username/password not correct"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# class LogoutView(APIView):
#     def post(self,request):
#         try:
#             logout(request)
#             return Response({"Message":"Logout Successfully"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# # @permission_classes([IsAuthenticated])

# @permission_classes([IsAuthenticated])
# class DashboardView(APIView):
#     def get(self,request):
#         try:
#             user = request.user.profile
#             return Response({"Message": "welcome" +" "+ user.fullname})
#         except Exception as e:
#             return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     