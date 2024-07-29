from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import LogoutSerializer, RegisterSerializer, MyTokenObtainPairSerializer
from users.tasks import get_verify_code


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer: RegisterSerializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})


class MyObtainTokenPairView(TokenObtainPairView):
    """Выступает в роли LoginView"""
    permission_classes = (AllowAny, )
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(generics.CreateAPIView):
    serializer_class = LogoutSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})


class VerifyCodeView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        get_verify_code.delay(request.user.email) #type: ignore
        return Response(status=status.HTTP_204_NO_CONTENT)
