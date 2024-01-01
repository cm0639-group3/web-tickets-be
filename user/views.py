from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserSerializer
from .serializers import ChangePasswordSerializer
from .serializers import AdminSerializer
from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny, IsAuthenticated , IsAdminUser
from django.contrib.auth import update_session_auth_hash


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {}
            data["message"] = "user registered successfully"
            data["email"] = user.email
            data["username"] = user.username
            token = Token.objects.get_or_create(user=user)[0].key
            # data["token"] = token     # -2dL

            return Response(data, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)      # -2dL       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request): 
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request): 
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): 
            user = User.objects.get(email = request.user.email)
            serializer = UserSerializer(user)
            return Response(serializer.data , status=status.HTTP_200_OK)
    def put(self, request):
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)


class AllUsersProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): 
        user = User.objects.all().values()
        serializer = UserSerializer(user, many=True)

        return Response(serializer.data , status=status.HTTP_200_OK)

class CreateAdminView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, format=None):
        serializer = AdminSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
