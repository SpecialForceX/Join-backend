from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from auth_user_app.api.serializer import RegistrationSerializer
from rest_framework import status
from django.contrib.auth import authenticate


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user, full_name = serializer.save()
            token, created = Token.objects.get_or_create(user=user)


            return Response({
                'token': token.key,
                'username': user.username,
                'id': user.id,
                'full_name': full_name
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(username=user.username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            full_name = user.userprofile.full_name if hasattr(user, 'userprofile') else ''

            return Response({
                "token": token.key,
                "username": user.username,
                "id": user.id,
                "full_name": full_name
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


