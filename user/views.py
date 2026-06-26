from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializer import RegisterSerializer, UserSerializer, SuperUserSerializer

User = get_user_model()



class SuperUserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if User.objects.filter(is_superuser=True).exists():
            return Response(
                {"error": "Superuser already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SuperUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(role=User.Role.ADMIN)
            return Response(
                {
                    "message": "Superuser created successfully.",
                    "user": SuperUserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Account created successfully.",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
